import json  # Importing the JSON module to work with JSON data
import boto3  # Importing the boto3 module to interact with AWS services
from hashlib import sha256  # Importing the sha256 function from hashlib to hash data
from botocore.config import Config  # Importing the Config class from botocore to configure AWS settings

# AWS SQS configuration
# Creating a configuration for AWS SQS with a specified region and retry strategy.
awsConfig = Config(
    region_name='us-east-1',  # Region name for AWS services
    retries={'max_attempts': 10, 'mode': 'standard'}  # Retry configuration
)

# Creating an SQS client to interact with the AWS SQS service
sqsClient = boto3.client('sqs', endpoint_url='http://localhost:4566', config=awsConfig)

# The URL of the SQS queue to interact with
queueUrl = 'http://localhost:4566/000000000000/login-queue'

def mask_data(value: str) -> str:
    """
    Masks the input value using SHA-256 hashing.
    Args:
    value (str): The value to be masked.
    Returns:
    str: The masked value.
    """
    return sha256(value.encode()).hexdigest()

def fetch_messages_from_sqs() -> list:
    """
    Reads messages from the SQS queue.
    Returns:
    list: A list of messages from the SQS queue.
    """
    # Receive messages from the SQS queue with a maximum of 10 messages and wait up to 10 seconds
    response = sqsClient.receive_message(
        QueueUrl=queueUrl,
        MaxNumberOfMessages=10,
        WaitTimeSeconds=10
    )
    # Return the list of messages received, or an empty list if no messages are found
    return response.get('Messages', [])

def handle_message(message: dict) -> tuple:
    """
    Processes a single message by masking PII and flattening the JSON object.
    Args:
    message (dict): The message to be processed.
    Returns:
    tuple: A tuple containing processed user data.
    """
    # Load the message body from JSON format to a Python dictionary
    body = json.loads(message['Body'])

    # Check if 'device_id' and 'ip' are present in the message
    if 'device_id' not in body or 'ip' not in body:
        return None

    # Mask the IP address and device ID
    maskedIp = mask_data(body['ip'])
    maskedDeviceId = mask_data(body['device_id'])

    # Return the processed user data as a tuple
    return (
        body['user_id'],
        body['device_type'],
        maskedIp,
        maskedDeviceId,
        body['locale'],
        body['app_version'],
        body['create_date']
    )

def remove_message_from_sqs(receiptHandle: str):
    """
    Deletes a message from the SQS queue.
    Args:
    receiptHandle (str): The receipt handle of the message to be deleted.
    """
    # Delete the message from the SQS queue using the receipt handle
    sqsClient.delete_message(
        QueueUrl=queueUrl,
        ReceiptHandle=receiptHandle
    )
