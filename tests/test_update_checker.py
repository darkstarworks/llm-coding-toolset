# From the root directory, run:
# python -m unittest tests.test_update_checker

import unittest
from unittest.mock import patch, MagicMock
from PyQt5.QtWidgets import QApplication, QMessageBox
from src.update_checker import check_for_updates, CURRENT_VERSION

class TestUpdateChecker(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    @patch('src.update_checker.requests.get')
    @patch('src.update_checker.QMessageBox.information')
    def test_update_available(self, mock_message_box, mock_get):
        # Mock the API response
        mock_response = MagicMock()
        mock_response.json.return_value = {"tag_name": "2.0.0"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Call the function
        check_for_updates()

        # Check if the correct message was displayed
        mock_message_box.assert_called_once_with(
            None, 
            "Update Available", 
            "A new version (2.0.0) is available. Please visit the GitHub repository to download the latest version."
        )

    @patch('src.update_checker.requests.get')
    @patch('src.update_checker.QMessageBox.information')
    def test_no_update_available(self, mock_message_box, mock_get):
        # Mock the API response
        mock_response = MagicMock()
        mock_response.json.return_value = {"tag_name": CURRENT_VERSION}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Call the function
        check_for_updates()

        # Check if the correct message was displayed
        mock_message_box.assert_called_once_with(
            None, 
            "No Updates", 
            "You are using the latest version."
        )

    @patch('src.update_checker.requests.get')
    @patch('src.update_checker.QMessageBox.warning')
    def test_request_exception(self, mock_message_box, mock_get):
        # Mock a request exception
        mock_get.side_effect = Exception("Connection error")

        # Call the function
        check_for_updates()

        # Check if the correct warning was displayed
        mock_message_box.assert_called_once_with(
            None, 
            "Update Check Failed", 
            "Failed to check for updates: Connection error"
        )

    @patch('src.update_checker.requests.get')
    @patch('src.update_checker.QMessageBox.warning')
    def test_invalid_json_response(self, mock_message_box, mock_get):
        # Mock an invalid JSON response
        mock_response = MagicMock()
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Call the function
        check_for_updates()

        # Check if the correct warning was displayed
        mock_message_box.assert_called_once_with(
            None, 
            "Update Check Failed", 
            "Failed to check for updates: Invalid JSON"
        )

    @patch('src.update_checker.requests.get')
    @patch('src.update_checker.QMessageBox.warning')
    def test_missing_tag_name(self, mock_message_box, mock_get):
        # Mock a response missing the tag_name
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Call the function
        check_for_updates()

        # Check if the correct warning was displayed
        mock_message_box.assert_called_once_with(
            None, 
            "Update Check Failed", 
            "Failed to check for updates: 'tag_name'"
        )

    @patch('src.update_checker.requests.get')
    @patch('src.update_checker.QMessageBox.information')
    def test_with_parent_widget(self, mock_message_box, mock_get):
        # Mock the API response
        mock_response = MagicMock()
        mock_response.json.return_value = {"tag_name": "2.0.0"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Create a mock parent widget
        mock_parent = MagicMock()

        # Call the function with a parent widget
        check_for_updates(mock_parent)

        # Check if the message box was called with the parent widget
        mock_message_box.assert_called_once_with(
            mock_parent, 
            "Update Available", 
            "A new version (2.0.0) is available. Please visit the GitHub repository to download the latest version."
        )

    # ... (other test methods)

if __name__ == '__main__':
    unittest.main()