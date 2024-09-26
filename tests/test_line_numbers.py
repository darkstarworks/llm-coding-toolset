# From the root directory, run:
# python -m unittest tests.test_line_numbers

import unittest
from unittest.mock import patch, MagicMock
from PyQt5.QtWidgets import QApplication
from src.line_numbers import LineNumbersTab

class TestLineNumbers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    def setUp(self):
        self.line_numbers_tab = LineNumbersTab()

    def test_initial_state(self):
        self.assertEqual(self.line_numbers_tab.file_input.text(), "")
        self.assertEqual(self.line_numbers_tab.start_line.value(), 1)
        self.assertEqual(self.line_numbers_tab.code_input.toPlainText(), "")
        self.assertEqual(self.line_numbers_tab.output.toPlainText(), "")

    @patch('PyQt5.QtWidgets.QFileDialog.getOpenFileName')
    def test_browse_file(self, mock_file_dialog):
        mock_file_dialog.return_value = ('/path/to/file.txt', '')
        
        with patch('builtins.open', unittest.mock.mock_open(read_data="file content")):
            self.line_numbers_tab.browse_file()
        
        self.assertEqual(self.line_numbers_tab.file_input.text(), '/path/to/file.txt')
        self.assertFalse(self.line_numbers_tab.start_line.isEnabled())
        self.assertEqual(self.line_numbers_tab.file_contents, "file content")

    def test_find_lines_for_snippet(self):
        self.line_numbers_tab.file_contents = "line1\nline2\nline3\nline4\nline5"
        
        # Test finding a snippet at the beginning
        self.assertEqual(self.line_numbers_tab.find_lines_for_snippet("line1\nline2"), 1)
        
        # Test finding a snippet in the middle
        self.assertEqual(self.line_numbers_tab.find_lines_for_snippet("line3\nline4"), 3)
        
        # Test not finding a snippet
        self.assertEqual(self.line_numbers_tab.find_lines_for_snippet("nonexistent"), -1)

    def test_add_line_numbers_without_file(self):
        self.line_numbers_tab.code_input.setPlainText("def example():\n    pass")
        self.line_numbers_tab.start_line.setValue(10)
        self.line_numbers_tab.add_line_numbers()
        
        expected_output = "10: def example():\n11:     pass"
        self.assertEqual(self.line_numbers_tab.output.toPlainText(), expected_output)

    def test_add_line_numbers_with_file(self):
        self.line_numbers_tab.file_contents = "line1\nline2\nline3\nline4\nline5"
        self.line_numbers_tab.code_input.setPlainText("line2\nline3")
        self.line_numbers_tab.add_line_numbers()
        
        expected_output = "2: line2\n3: line3"
        self.assertEqual(self.line_numbers_tab.output.toPlainText(), expected_output)

    def test_add_line_numbers_snippet_not_found(self):
        self.line_numbers_tab.file_contents = "line1\nline2\nline3"
        self.line_numbers_tab.code_input.setPlainText("nonexistent")
        self.line_numbers_tab.add_line_numbers()
        
        expected_output = "Snippet not found in the loaded file."
        self.assertEqual(self.line_numbers_tab.output.toPlainText(), expected_output)

    @patch('pyperclip.copy')
    def test_copy_to_clipboard(self, mock_copy):
        self.line_numbers_tab.output.setPlainText("1: test\n2: output")
        self.line_numbers_tab.copy_to_clipboard()
        
        mock_copy.assert_called_once_with("1: test\n2: output")

    # ... (other test methods)

if __name__ == '__main__':
    unittest.main()