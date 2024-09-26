# update_checker.py
# This module provides functionality to check for updates to the application.

import requests
from PyQt5.QtWidgets import QMessageBox

CURRENT_VERSION = "1.0.0"
UPDATE_URL = "https://api.github.com/repos/darkstarworks/llm-coding-toolset/releases/latest"

def check_for_updates(parent=None):
    """
    Check for updates by comparing the current version with the latest release on GitHub.
    
    Args:
        parent (QWidget): The parent widget for displaying message boxes.
    """
    try:
        response = requests.get(UPDATE_URL)
        response.raise_for_status()
        latest_version = response.json()["tag_name"]
        
        if latest_version > CURRENT_VERSION:
            QMessageBox.information(parent, "Update Available", 
                                    f"A new version ({latest_version}) is available. "
                                    "Please visit the GitHub repository to download the latest version.")
        else:
            QMessageBox.information(parent, "No Updates", "You are using the latest version.")
    except Exception as e:
        QMessageBox.warning(parent, "Update Check Failed", f"Failed to check for updates: {str(e)}")