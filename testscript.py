import json
import boto3
import psycopg2
from hashlib import sha256
from botocore.config import Config

# AWS SQS configuration
# Creating a configuration for AWS SQS with a specified region and retry strategy.
awsConfig = Config(
    region_name='us-east-1',  # Region name for AWS services
    retries={'max_attempts': 10, 'mode': 'standard'}  # Retry configuration
)
sqsClient = boto3.client('sqs', endpoint_url='http://localhost:4566', config=awsConfig)
queueUrl = 'http://localhost:4566/000000000000/login-queue'

# Postgres configuration
connection = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)
dbCursor = connection.cursor()

# Altering user_logins table to change app_version data type from integer to varchar
# to save the data as it is coming from the queue without changing the format
dbCursor.execute("""
    ALTER TABLE user_logins
    ALTER COLUMN app_version TYPE varchar(32)
""")


def maskData(value: str) -> str:
    """
    Masks the input value using SHA-256 hashing.
    Args:
    value (str): The value to be masked.
    Returns:
    str: The masked value.
    """
    return sha256(value.encode()).hexdigest()


def fetchMessagesFromSqs() -> list:
    """
    Reads messages from the SQS queue.
    Returns:
    list: A list of messages from the SQS queue.
    """
    response = sqsClient.receive_message(
        QueueUrl=queueUrl,
        MaxNumberOfMessages=10,  # Maximum number of messages to return in a single call
        WaitTimeSeconds=10  # Long polling to wait up to 10 seconds for messages to arrive
    )
    # Return the list of messages received, or an empty list if no messages are found
    return response.get('Messages', [])


def handleMessage(message: dict) -> tuple:
    """
    Processes a single message by masking PII and flattening the JSON object.
    Args:
    message (dict): The message to be processed.
    Returns:
    tuple: A tuple containing processed user data.
    """
    body = json.loads(message['Body'])

    # Check if 'device_id' and 'ip' are present
    if 'device_id' not in body or 'ip' not in body:
        return None

    maskedIp = maskData(body['ip'])
    maskedDeviceId = maskData(body['device_id'])

    return (
        body['user_id'],
        body['device_type'],
        maskedIp,
        maskedDeviceId,
        body['locale'],
        body['app_version'],  # app_version as string
        body['create_date']
    )


def insertIntoPostgres(userData: tuple):
    """
    Inserts processed user data into the Postgres database.
    Args:
    userData (tuple): The processed user data to be inserted.
    """
    dbCursor.execute("""
        INSERT INTO user_logins (user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, userData)


def removeMessageFromSqs(receiptHandle: str):
    """
    Deletes a message from the SQS queue.
    Args:
    receiptHandle (str): The receipt handle of the message to be deleted.
    """
    sqsClient.delete_message(
        QueueUrl=queueUrl,
        ReceiptHandle=receiptHandle
    )


def main():
    """
    Main function to orchestrate reading from SQS, processing messages, and inserting into Postgres.
    """
    messages = fetchMessagesFromSqs()
    for message in messages:
        userData = handleMessage(message)
        if userData:
            insertIntoPostgres(userData)
            removeMessageFromSqs(message['ReceiptHandle'])  # To prevent message from reprocessing and duplication of data in database.

    connection.commit()
    dbCursor.close()
    connection.close()


if __name__ == "__main__":
    main()
