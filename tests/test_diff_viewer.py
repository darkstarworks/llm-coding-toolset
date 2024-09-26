# From the root directory, run:
# python -m unittest tests.test_diff_viewer

import unittest
from unittest.mock import patch, MagicMock
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QSize
from src.diff_viewer import DiffViewerTab, DiffViewer

class TestDiffViewer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    def setUp(self):
        self.diff_viewer_tab = DiffViewerTab()

    def test_initial_state(self):
        self.assertEqual(self.diff_viewer_tab.text1.toPlainText(), "")
        self.assertEqual(self.diff_viewer_tab.text2.toPlainText(), "")

    @patch('PyQt5.QtWidgets.QFileDialog.getOpenFileName')
    def test_load_file(self, mock_file_dialog):
        mock_file_dialog.return_value = ('/path/to/file.txt', '')
        
        with patch('builtins.open', unittest.mock.mock_open(read_data="file content")):
            self.diff_viewer_tab.load_file(1)
        
        self.assertEqual(self.diff_viewer_tab.text1.toPlainText(), "file content")

        with patch('builtins.open', unittest.mock.mock_open(read_data="another content")):
            self.diff_viewer_tab.load_file(2)
        
        self.assertEqual(self.diff_viewer_tab.text2.toPlainText(), "another content")

    def test_compare_texts(self):
        self.diff_viewer_tab.text1.setPlainText("line1\nline2\nline3")
        self.diff_viewer_tab.text2.setPlainText("line1\nmodified\nline3")

        # Mock the set_diff method of DiffViewer
        self.diff_viewer_tab.diff_viewer.set_diff = MagicMock()

        self.diff_viewer_tab.compare_texts()

        # Check if set_diff was called with the correct diff
        expected_diff = [
            '--- ',
            '+++ ',
            '@@ -1,3 +1,3 @@',
            ' line1',
            '-line2',
            '+modified',
            ' line3'
        ]
        self.diff_viewer_tab.diff_viewer.set_diff.assert_called_once_with(expected_diff)

class TestDiffViewerWidget(unittest.TestCase):
    def setUp(self):
        self.diff_viewer = DiffViewer()

    def test_set_diff(self):
        diff = [
            '--- ',
            '+++ ',
            '@@ -1,3 +1,3 @@',
            ' line1',
            '-line2',
            '+modified',
            ' line3'
        ]
        self.diff_viewer.set_diff(diff)
        self.assertEqual(self.diff_viewer.diff_lines, diff[2:])  # Excluding metadata lines

    def test_size_hint(self):
        self.diff_viewer.diff_lines = ['line1', 'line2', 'line3']
        expected_size = QSize(600, 3 * 20)  # 3 lines * 20 pixels per line
        self.assertEqual(self.diff_viewer.sizeHint(), expected_size)

    @patch('PyQt5.QtGui.QPainter')
    def test_paint_event(self, mock_painter):
        self.diff_viewer.diff_lines = [
            '@@ -1,3 +1,3 @@',
            ' line1',
            '-line2',
            '+modified',
            ' line3'
        ]
        mock_event = MagicMock()
        
        # Create a mock painter object
        mock_painter_instance = MagicMock()
        mock_painter.return_value = mock_painter_instance

        # Mock the font metrics
        mock_font_metrics = MagicMock()
        mock_font_metrics.height.return_value = 15
        mock_painter_instance.fontMetrics.return_value = mock_font_metrics

        self.diff_viewer.paintEvent(mock_event)

        # Check if the correct number of lines were drawn
        self.assertEqual(mock_painter_instance.drawText.call_count, 5)

        # Check if the correct colors were set for different line types
        color_calls = mock_painter_instance.setPen.call_args_list
        self.assertEqual(len(color_calls), 5)  # 5 lines, 5 color settings

    # ... (other test methods)

if __name__ == '__main__':
    unittest.main()