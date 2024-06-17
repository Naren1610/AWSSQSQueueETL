import unittest  # Importing the unittest module for creating and running tests
from unittest.mock import patch  # Importing patch to mock objects and functions
from src.dbHandler import insert_into_postgres

class TestDbHandler(unittest.TestCase):

    @patch('src.dbHandler.dbCursor.execute')
    def test_insert_into_postgres(self, mock_execute):
        # Mocking user data to be inserted
        userData = (
            'test_user', 'android', 'masked_ip', 'masked_device_id', 'US', '1.0.0', '2024-01-01'
        )
        # Calling the function to insert user data into the database
        insert_into_postgres(userData)
        # Asserting that the execute method was called once
        mock_execute.assert_called_once()

if __name__ == '__main__':
    unittest.main()  # Running the tests if this script is executed
