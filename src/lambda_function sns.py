import requests
import logging
import os
import json
import re

# Configure logging
logger = logging.getLogger()
log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()
logger.setLevel(getattr(logging, log_level, logging.INFO))

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
            "kevin.buckley.texas": "18175839958"
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
        # Log the final list of phone numbers
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
    logger.info("START of Lambda CODE")

    logger.info(f"The Event: {event}")
    logger.info("Parse Event")

    try:
        if 'Records' in event and event['Records'][0].get('EventSource') == 'aws:sns':
            logger.info("Detected SNS event, extracting SES event from Message")
            sns_message = event['Records'][0]['Sns']['Message']
            # Parse the JSON string in the Message field
            ses_event = json.loads(sns_message)
        else:
            logger.info("Assuming direct SES event")
            ses_event = event
    except (KeyError, json.JSONDecodeError) as e:
        logger.error(f"Error processing event: {str(e)}")
        return {
            'statusCode': 400,
            'body': f'Invalid event format: {str(e)}'
        }

    logger.info("Parse Event")
    to_number_list, from_addr, subj = parse_ses_event(ses_event)
    
    #to_number_list, from_addr, subj = parse_ses_event(event)

    message = subj

    if to_number_list is None or from_addr is None or subj is None:
        logger.info("Invalid SES Event Format")
        return {
            'statusCode': 400,
            'body': 'Invalid SES event format'
        }   
    else:
        send_sms(from_number,to_number_list,message)

    return {
        'statusCode': 200,
        'body': 'SMS sent successfully!'
    }
    