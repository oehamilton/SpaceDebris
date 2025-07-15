import requests
import logging
import os
import json
import re
import boto3
import base64
import email
from email import policy
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from email.utils import getaddresses

# Configure logging (unchanged)
logger = logging.getLogger()
log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()
logger.setLevel(getattr(logging, log_level, logging.INFO))
handler = logging.StreamHandler()
formatter = logging.Formatter('{"level": "%(levelname)s", "timestamp": "%(asctime)s", "message": %(message)s}')
handler.setFormatter(formatter)
logger.handlers = [handler]

# Your send_sms function (unchanged)
def send_sms(from_number, to_number, message):
    url = "https://sms.api.sinch.com/xms/v1/d55362c23fe94a76a79a4409e249c85a/batches"
    headers = {
        "Authorization": "Bearer 6081f3c378b745e69b507e4c1eabdc4d",
        "Content-Type": "application/json"
    }
    logger.info(f"Extracted From address: {to_number}")
    print(message, from_number, to_number)
    data = {
        "from": from_number,
        "to": to_number,
        "body": message 
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        return {
            'statusCode': response.status_code,
            'body': response.text
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }

# Updated: Now attempts to find the correct HTML part by checking if it contains the expected 'ctrl_name' div.
def extract_alarm_message(msg):
    message_to_send = "Test alarm message - Othell Sandbox"
    logger.info("Starting Alarm search")  
    # Initialize variables
    alarm_msg = ""
    ctrl_name = ""
    ctrl_loc = ""
    alarms = []
    date_info = ""
    html_content = ""

    # Extract HTML content from potential parts, checking for the key div
    found = False
    if msg.is_multipart():
        logger.info("Message is multipart. Parts: %s", [part.get_content_type() for part in msg.walk()])
        for part in msg.walk():
            filename = part.get_filename()
            content_type = part.get_content_type()
            content_disposition = part.get('Content-Disposition', '')
            logger.info("Part - Filename: %s, Content-Type: %s, Disposition: %s", filename, content_type, content_disposition)

            candidate = None
            if filename and filename.lower().endswith('.htm'):
                logger.debug("Found .htm attachment")
                candidate = part.get_payload(decode=True).decode('utf-8', errors='ignore')
            elif content_disposition.startswith('attachment') and content_type in ['text/html', 'application/octet-stream']:
                logger.debug("Found attachment with HTML or octet-stream content")
                candidate = part.get_payload(decode=True).decode('utf-8', errors='ignore')
            elif content_type == 'text/html':
                logger.debug("Found text/html part")
                candidate = part.get_payload(decode=True).decode('utf-8', errors='ignore')

            if candidate:
                logger.debug("Trying candidate HTML for parsing")
                # Parse with BeautifulSoup
                try:
                    soup = BeautifulSoup(candidate, 'lxml')
                except Exception:
                    soup = BeautifulSoup(candidate, 'html.parser')

                # Check for ctrl_name
                ctrl_name_div = soup.find('div', attrs={'class': 'ctrl_name'})
                if ctrl_name_div:
                    html_content = candidate
                    found = True
                    logger.debug("Found matching HTML with ctrl_name")
                    break  # Use this one
                else:
                    logger.debug("Candidate does not contain ctrl_name; skipping")

    else:
        logger.debug("Message is not multipart. Content-Type: %s", msg.get_content_type())
        if msg.get_content_type() == 'text/html':
            html_content = msg.get_payload(decode=True).decode('utf-8', errors='ignore')

    if not found and html_content == "":
        logger.warning("No suitable HTML content found for alarm extraction")

    # Now parse the selected html_content
    if html_content:
        # Debug: Print raw HTML to verify
        # logger.debug("Raw HTML: %s", html_content)

        try:
            soup = BeautifulSoup(html_content, 'lxml')
        except Exception:
            soup = BeautifulSoup(html_content, 'html.parser')

        # Extract ctrl_name
        ctrl_name_div = soup.find('div', attrs={'class': 'ctrl_name'})
        if ctrl_name_div:
            ctrl_name = ctrl_name_div.get_text(strip=True) 
        logger.debug(f"Extracted ctrl_name: {ctrl_name}")

        # Extract ctrl_loc
        ctrl_loc_div = soup.find('div', class_='ctrl_loc')
        if ctrl_loc_div:
            ctrl_loc = ctrl_loc_div.get_text(strip=True)

        # Extract date information
        edate_div = soup.find('div', class_='edate-content')
        if edate_div:
            weekday = edate_div.find('div', class_='weekday')
            day = edate_div.find('div', class_='day')
            if weekday and day:
                date_info = f"{weekday.get_text(strip=True)} {day.get_text(strip=True)}"

        # Extract alarms
        alarm_header = soup.find('div', class_='box-header-alarm')
        if alarm_header:
            alarm_content = alarm_header.find_next_sibling('div', class_='box-content')
            if alarm_content:
                alarm_divs = alarm_content.find_all('div', class_='box-alarm-on')
                alarms = [alarm.get_text(strip=True) for alarm in alarm_divs]

        # Construct the alarm_msg
        if ctrl_name and alarms:
            alarm_msg = f"{ctrl_name} ({ctrl_loc}) - Alarms: {', '.join(alarms)}"

    logger.debug(f"Extracted message_to_send: {alarm_msg}")       
    message_to_send = alarm_msg[:160]    
    return message_to_send

# Refactored: Now takes raw bytes from S3, parses the full email, extracts To/Subject, processes phone numbers, and gets alarm from attachment.
def parse_sns_event(sns_message_bytes): 
    to_number_list = []
    message_2_send = None

    ######################################################### 
    logger.info("Starting Parse SNS Message")
    
    # Parse the raw email bytes
    msg = email.message_from_bytes(sns_message_bytes, policy=policy.default)
    
    # Extract the From address
    from_header = msg.get('From', '')
    from_list = getaddresses([from_header])
    from_emails = [addr.strip() for name, addr in from_list if addr]
    logger.info(f"Extracted From address: {from_emails}")
    from_name = from_emails[0].split('@')[0] if from_emails else None
    logger.info(f"Extracted From address: {from_name}")
    if from_name is None:
        logger.error("Failed to extract From address")
        return [], None

    # Extract To addresses (destination)
    to_header = msg.get('To', '')
    destination_list = getaddresses([to_header])
    destination_emails = [addr.strip() for name, addr in destination_list if addr]
    logger.info(f"Extracted destinations: {destination_emails}")

    # Extract phone numbers from all destination email addresses
    for destination in destination_emails:
        try:
            dest_phone_number, _ = destination.split('@')  # Split to extract the local part
            logger.info(f"Extracted dest_phone_number: {dest_phone_number}")
            if dest_phone_number and re.match(r'^\d{10}$', dest_phone_number):  # Check if it's a 10-digit phone number
                to_number_list.append(dest_phone_number)
        except ValueError:
            logger.debug(f"Skipping invalid email format: {destination}")
            continue

    # Ensure numbers are in E.164 format (+1 prefix) and unique
    to_number_list = [f"1{number}" for number in to_number_list if number and re.match(r'^\d{10}$', number)]
    to_number_list = list(set(to_number_list))  # Remove duplicates
    logger.info(f"Final to_number_list: {to_number_list}")

    # Extract Subject
    subject = msg.get('Subject', '')
    logger.info(f"Extracted Subject: {subject}")
    
    # Extract message from attachment
    message_2_send = extract_alarm_message(msg)
    logger.info(f"Extracted message: {message_2_send}")

    if message_2_send is None or not message_2_send.strip():
        message_2_send = "{} {}".format(from_name, subject)
        logger.info(f"Falling back to subject as message: {message_2_send}")
    
    return to_number_list, message_2_send

# Your lambda_handler (updated SNS path only; direct SES path unchanged)
def lambda_handler(event, context):
    from_number = '12085797066' 
    to_number = '19402063925'
    from_addr = 'none'
    logger.info("START of Lambda CODE")

    logger.info(f"The Event: {event}")
    logger.info("Parse Event")

    try:
        if 'Records' in event and event['Records'][0].get('EventSource') == 'aws:sns':
            logger.info("Detected SNS event, extracting SES event from Message")
            sns_message = json.loads(event['Records'][0]['Sns']['Message'])
            # Get Bucket Name and objectKey
            bucket_name = sns_message['receipt']['action']['bucketName']
            object_key = sns_message['receipt']['action']['objectKey']
            logger.info(f"Bucket Name: {bucket_name}")
            logger.info(f"Object Key: {object_key}")
            # Get the file from S3
            s3 = boto3.client('s3')  # Initialize S3 client
            response = s3.get_object(Bucket=bucket_name, Key=object_key)
            logger.info(f"Response: {response}")
            # Read the content of the file (keep as bytes!)
            file_content = response['Body'].read()  # This is bytes
            logger.info(f"File Content length: {len(file_content)} bytes")  # Log length instead of full content to avoid large logs

            to_number_list, message_2_send = parse_sns_event(file_content)

            logger.info(f"Extracted message: {message_2_send}")
            logger.info(f"Extracted to_number_list: {to_number_list}")
        else:
            logger.info("Assuming direct SES event")
            ses_event = event
            to_number_list, from_addr, message_2_send = parse_ses_event(ses_event)
            logger.info(f"Extracted From address: {from_addr}")
            logger.info(f"Extracted message: {message_2_send}")
            logger.info(f"Extracted to_number_list: {to_number_list}")

    except (KeyError, json.JSONDecodeError) as e:
        logger.error(f"Error processing event: {str(e)}")
        return {
            'statusCode': 400,
            'body': f'Invalid event format: {str(e)}'
        }

    logger.info("Parse Event Completed")

    if to_number_list is None or message_2_send is None:
        logger.info("Invalid SES Event Format")
        return {
            'statusCode': 400,
            'body': 'Invalid SES event format'
        }   
    else:
        logger.info(f"Sending SMS") 
        #send_sms(from_number,to_number_list,message_2_send) 
        logger.info(f"Extracted From number: {from_number}")
        logger.info(f"Extracted to_number_list: {to_number_list}")
        logger.info(f"Extracted message: {message_2_send}")
    return {
        'statusCode': 200,
        'body': 'SMS sent successfully!'
    }