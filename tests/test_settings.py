# From the root directory, run:
# python -m unittest tests.test_settings

import unittest
from unittest.mock import patch, MagicMock
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QSettings
from src.settings import SettingsDialog

class TestSettingsDialog(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    def setUp(self):
        self.mock_settings = MagicMock(spec=QSettings)
        with patch('src.settings.QSettings', return_value=self.mock_settings):
            self.dialog = SettingsDialog()

    def test_initial_state(self):
        # Test that all UI elements are created
        self.assertIsNotNone(self.dialog.theme_combo)
        self.assertIsNotNone(self.dialog.depth_combo)
        self.assertIsNotNone(self.dialog.auto_update_check)

        # Test that theme combo has correct items
        self.assertEqual(self.dialog.theme_combo.count(), 2)
        self.assertEqual(self.dialog.theme_combo.itemText(0), "Light")
        self.assertEqual(self.dialog.theme_combo.itemText(1), "Dark")

        # Test that depth combo has correct items
        self.assertEqual(self.dialog.depth_combo.count(), 10)
        for i in range(10):
            self.assertEqual(self.dialog.depth_combo.itemText(i), str(i + 1))

    @patch('src.settings.QSettings')
    def test_load_settings_default(self, mock_qsettings):
        # Mock QSettings to return default values
        mock_settings = MagicMock()
        mock_settings.value.side_effect = ["Light", "3", True]
        mock_qsettings.return_value = mock_settings

        dialog = SettingsDialog()

        self.assertEqual(dialog.theme_combo.currentText(), "Light")
        self.assertEqual(dialog.depth_combo.currentText(), "3")
        self.assertTrue(dialog.auto_update_check.isChecked())

    @patch('src.settings.QSettings')
    def test_load_settings_custom(self, mock_qsettings):
        # Mock QSettings to return custom values
        mock_settings = MagicMock()
        mock_settings.value.side_effect = ["Dark", "5", False]
        mock_qsettings.return_value = mock_settings

        dialog = SettingsDialog()

        self.assertEqual(dialog.theme_combo.currentText(), "Dark")
        self.assertEqual(dialog.depth_combo.currentText(), "5")
        self.assertFalse(dialog.auto_update_check.isChecked())

    def test_save_settings(self):
        # Set up the dialog with some values
        self.dialog.theme_combo.setCurrentText("Dark")
        self.dialog.depth_combo.setCurrentText("7")
        self.dialog.auto_update_check.setChecked(False)

        # Call save_settings
        self.dialog.save_settings()

        # Check that QSettings.setValue was called with the correct values
        self.mock_settings.setValue.assert_any_call("theme", "Dark")
        self.mock_settings.setValue.assert_any_call("default_depth", "7")
        self.mock_settings.setValue.assert_any_call("auto_update", False)

    @patch('src.settings.QSettings')
    def test_accept_calls_save_settings(self, mock_qsettings):
        mock_settings = MagicMock()
        mock_qsettings.return_value = mock_settings

        dialog = SettingsDialog()
        
        # Mock the save_settings method
        dialog.save_settings = MagicMock()

        # Call accept (this is what happens when you click "Save")
        dialog.accept()

        # Check that save_settings was called
        dialog.save_settings.assert_called_once()

    # ... (other test methods)

if __name__ == '__main__':
    unittest.main()