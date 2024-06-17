import unittest  # Importing the unittest module for creating and running tests
from unittest.mock import patch, MagicMock  # Importing patch and MagicMock to mock objects and functions
from src.sqsHandler import fetch_messages_from_sqs, handle_message, mask_data

class TestSqsHandler(unittest.TestCase):

    @patch('src.sqsHandler.sqsClient.receive_message')
    def test_fetch_messages_from_sqs(self, mock_receive_message):
        # Mocking the response from the SQS client
        mock_receive_message.return_value = {
            'Messages': [
                {
                    'Body': '{"user_id": "test_user", "device_id": "test_device", "ip": "192.168.0.1", "device_type": "android", "locale": "US", "app_version": "1.0.0", "create_date": "2024-01-01"}',
                    'ReceiptHandle': 'mock_receipt_handle'
                }
            ]
        }
        # Calling the function to fetch messages from SQS
        messages = fetch_messages_from_sqs()
        # Asserting that one message was returned
        self.assertEqual(len(messages), 1)
        # Asserting that the message contains the 'Body' key
        self.assertIn('Body', messages[0])

    def test_handle_message(self):
        # Mocking a message to be processed
        message = {
            'Body': '{"user_id": "test_user", "device_id": "test_device", "ip": "192.168.0.1", "device_type": "android", "locale": "US", "app_version": "1.0.0", "create_date": "2024-01-01"}'
        }
        # Calling the function to handle the message
        userData = handle_message(message)
        # Asserting that the returned data contains 7 elements
        self.assertEqual(len(userData), 7)
        # Asserting that the user_id matches the expected value
        self.assertEqual(userData[0], 'test_user')

    def test_mask_data(self):
        # Defining a value to be masked
        value = 'test_value'
        # Calling the function to mask the value
        masked_value = mask_data(value)
        # Asserting that the length of the masked value is 64 characters (SHA-256 hash length)
        self.assertEqual(len(masked_value), 64)

if __name__ == '__main__':
    unittest.main()  # Running the tests if this script is executed
