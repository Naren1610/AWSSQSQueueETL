from sqsHandler import fetch_messages_from_sqs, handle_message, remove_message_from_sqs
from dbHandler import insert_into_postgres, alter_table, commit_and_close

def main():
    """
    Main function to orchestrate reading from SQS, processing messages, and inserting into Postgres.
    """
    alter_table()  # Alter the table structure if needed
    messages = fetch_messages_from_sqs()  # Fetch messages from SQS queue
    for message in messages:
        userData = handle_message(message)  # Process each message
        if userData:
            insert_into_postgres(userData)  # Insert processed data into the database
            remove_message_from_sqs(message['ReceiptHandle'])  # Remove the message from the SQS queue

    commit_and_close()  # Commit changes and close the database connection

if __name__ == "__main__":
    main()  # Run the main function if this script is executed
