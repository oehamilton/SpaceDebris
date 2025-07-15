import requests
import logging
import os
import json
import re
#import boto3
import base64
import email
from email import policy
from datetime import datetime, timedelta
import requests
import logging
import os
import json
import re
#import boto3
import base64
import email
from email import policy
from datetime import datetime, timedelta
import email.policy
from bs4 import BeautifulSoup

# Configure logging
logger = logging.getLogger()
log_level = os.environ.get('LOG_LEVEL', 'DEBUG').upper()
logger.setLevel(getattr(logging, log_level, logging.DEBUG))

# Optional: Use JSON formatting for structured logging
handler = logging.StreamHandler()
formatter = logging.Formatter('{"level": "%(levelname)s", "timestamp": "%(asctime)s", "message": %(message)s}')
handler.setFormatter(formatter)
logger.handlers = [handler]


def send_sms(from_number, to_number, message):
    url = "https://sms.api.sinch.com/xms/v1/d55362c23fe94a76a79a4409e249c85a/batches"
    headers = {
        "Authorization": "Bearer 6081f3c378b745e69b507e4c1eabdc4d",
        "Content-Type": "application/json"
    }

    logger.info(f"Extracted From address: {to_number}")

    print(message,from_number,to_number )
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

def extract_latest_reply(email_content):
    # Split the content into lines
    logger.debug(f"Extracted email_content: {email_content}")
    lines = email_content.split('\n')
              
    # Define a regex pattern to match "\ufeffOn [date], [time], xxx wrote:" more precisely
    pattern = r'\ufeff?On .+, .+ wrote:'
              
    # Find the index of the line matching the pattern
    cut_off_index = next((i for i, line in enumerate(lines) if re.match(pattern, line.strip())), len(lines))
              
    # Keep only the lines before the cut-off point and remove quoted lines
    latest_reply_lines = []
    for line in lines[:cut_off_index]:
        stripped_line = line.strip()
    if not stripped_line.startswith('>') and not stripped_line.startswith('&gt;'):
        latest_reply_lines.append(line)
              
    # Remove any trailing empty lines
    while latest_reply_lines and not latest_reply_lines[-1].strip():
        latest_reply_lines.pop()
              
    # Join the remaining lines
    latest_reply = '\n'.join(latest_reply_lines).strip()
    logger.debug(f"Extracted latest_reply: {latest_reply}")
           
    return latest_reply

def extract_email_body(sns_message):
    message_to_send = "Test alarm message"
    #Get Alarm Message from SNS message and shorten it to 160 characters
    
    content = sns_message['content'] # Get the base64 encoded content           
    decoded_content = base64.b64decode(content) # Decode the base64 content              
    msg = email.message_from_bytes(decoded_content, policy=policy.default) # Parse the email message
        #Get attachment from email message
    attachment = msg.get_payload()[1]
        #parse attattachment
    attachment_content = attachment.get_payload(decode=True).decode('utf-8')
        #parse attachment_content as htm
    attachment_html = email.message_from_string(attachment_content, policy=policy.default)
        #get body of attachment_html
    attachment_body = attachment_html.get_payload()[0].get_payload(decode=True).decode('utf-8')
    logger.debug(f"Extracted attachment_body: {attachment_body}")
        #find Alarm Message in attachment_body
    alarm_message = attachment_body.split('box-header-alarm')[1].split('Alarms')[0]
    logger.debug(f"Extracted alarm_message: {alarm_message}")

    #logger.debug(f"Extracted message: {msg}") 

    #extract_email_body = extract_latest_reply(msg.get_body(preferencelist=('plain',)).get_content())
    #logger.debug(f"Extracted extract_email_body: {extract_email_body}")
    

    
    message_to_send = extract_email_body[:160]

    logger.debug(f"Extracted message_to_send: {message_to_send}")

    ''' Search and extract from the email msg for these values
            Kurita
            TCCD
            Kurita Advisor Login
                Systems Status
            0 Critical Events
            0 Warning Events
            Device Status
            1 of 1 Device Connected
            0 Device Issues
    '''
    


    return message_to_send


def parse_sns_event(sns_message): 
    to_number_list=[]
    from_address= None
    message_2_send= None
    
    try:
        logger.debug("Starting Parse SNS Message")
        message_2_send = extract_email_body(sns_message)
        logger.debug(f"Extracted message: {message_2_send}")

        destination = sns_message['mail']['destination'][0] # Extract the first destination email address
        logger.debug(f"Extracted destination: {destination}")
        dest_phone_number, x = destination.split('@') # Split the destination email address to extract the phone number
        logger.debug(f"Extracted dest_phone_number: {dest_phone_number}")
        #to_addresses_list = [email.split('@')[0] for email in destination] # Extract local parts of destination email addresses
        #logger.debug(f"Extracted to_addresses_list: {to_addresses_list}")
        #Add destination phone number to list of numbers
        if dest_phone_number and re.match(r'^\d{10}$', dest_phone_number): # If email recipient is a 10 digit phone number, add it directly
            to_number_list.append(dest_phone_number)
        #to_number_list += dest_phone_number # If email recipient is a 10 digit phone number, add it directly
        to_number_list = [f"1{number}" for number in to_number_list if number and re.match(r'^\d{10}$', number)] # Ensure numbers are in E.164 format
        to_number_list = list(set(to_number_list))  # Ensure unique numbers
        logger.info(f"Final to_number_list: {to_number_list}")

        return to_number_list, message_2_send
    
    except (KeyError, json.JSONDecodeError) as e:
        logger.error(f"Error parsing SNS event: {str(e)}")
        return None, None, None
    



def parse_ses_event(event):
    """
    Parse To, From, and Subject from an AWS SES event.
    
    Args:
        event (dict): The AWS SES event dictionary
        
    Returns:
        tuple: (to_address, from_address, subject)
    """
    try:
        logger.debug("Starting Parse Script")
        # Define email-to-phone number mappings
        email_to_phone = {
            "oehamilton": "19402063925",
            "a.castillo": "16822068114",
            "kevin.buckley.texas": "18175839985"
            # Add more mappings here as needed, e.g.,
            # "another.user": "12345678901",
        }

        logger.debug(f"Email-to-phone mappings: {email_to_phone}")

        # Navigate to the commonHeaders section where the fields are located
        headers = event['Records'][0]['ses']['mail']['commonHeaders']
        destination = event['Records'][0]['ses']['mail']['destination']

        # Extract the fields

        # Extract From email address (e.g., "sender@FromCompany.com" from "\"Doe, John\" <sender@FromCompany.com>")
        from_field = headers['from'][0]
        
        # Use regex to extract email address from formats like "Name <email>" or plain email
        email_match = re.search(r'[\w\.-]+@[\w\.-]+', from_field)
        from_address = email_match.group(0) if email_match else from_field
        logger.info(f"Extracted From address: {from_address}")


        subject = headers['subject']
        logger.info(f"Extracted Subject: {subject}")


        # Extract local parts of destination email addresses
        to_addresses_list = [email.split('@')[0] for email in destination]
        logger.info(f"Extracted to name list {to_addresses_list}")


        # Build to_number_list using dictionary lookup
        to_number_list = [email_to_phone.get(address) for address in to_addresses_list if address in email_to_phone]
        logger.info(f"Generated to_number_list: {to_number_list}")

        #If email recipient is a 10 digit phone number, add it directly
        to_number_list += [address for address in to_addresses_list if re.match(r'^\d{10}$', address)]
        
        #All numbers in the list should be 1 plus the 10 digit phone number
        to_number_list = [f"1{number}" for number in to_number_list if number and re.match(r'^\d{10}$', number)]
        logger.info(f"Numbers in to_number_list: {to_number_list}")

        #All the numbers in the list should be unique
        to_number_list = list(set(to_number_list))  
        logger.info(f"Final to_number_list: {to_number_list}")

        # If no valid phone numbers were found, return None
        if not to_number_list:
            logger.warning("No valid phone numbers found in the email addresses.")
            return None, None, None 

        # Log unmapped addresses for debugging
        unmapped = [address for address in to_addresses_list if address not in email_to_phone]
        if unmapped:
            logger.warning(f"Unmapped email addresses: {unmapped}")


        return to_number_list, from_address, subject

    except (KeyError, IndexError) as e:
        print(f"Error parsing event: {str(e)}")
        return None, None, None

def lambda_handler(event, context):
    from_number= '12085797066' 
    to_number = '19402063925'
    from_addr = 'none'
    logger.info("START of Lambda CODE")

    logger.info(f"The Event: {event}")
    logger.info("Parse Event")

    try:
        if 'Records' in event and event['Records'][0].get('EventSource') == 'aws:sns':
            logger.info("Detected SNS event, extracting SES event from Message")
            sns_message = json.loads(event['Records'][0]['Sns']['Message'])
            to_number_list, message_2_send = parse_sns_event(sns_message)
            logger.info(f"Extracted Subject: {message_2_send}")
            logger.info(f"Extracted to_number_list: {to_number_list}")
        else:
            logger.info("Assuming direct SES event")
            ses_event = event
            to_number_list, from_addr, message_2_send = parse_ses_event(ses_event)
            logger.info(f"Extracted From address: {from_addr}")
            logger.info(f"Extracted Subject: {message_2_send}")
            logger.info(f"Extracted to_number_list: {to_number_list}")

    except (KeyError, json.JSONDecodeError) as e:
        logger.error(f"Error processing event: {str(e)}")
        return {
            'statusCode': 400,
            'body': f'Invalid event format: {str(e)}'
        }

    logger.info("Parse Event Completed")

    if to_number_list is None or from_addr is None or message_2_send is None:
        logger.info("Invalid SES Event Format")
        return {
            'statusCode': 400,
            'body': 'Invalid SES event format'
        }   
    else:
        send_sms(from_number,to_number_list,message_2_send)
        logger.info("Sending SMS")  
    return {
        'statusCode': 200,
        'body': 'SMS sent successfully!'
    }
    