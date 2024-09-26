# settings.py
# This module provides a dialog for managing user settings.

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QComboBox, QCheckBox, QPushButton)
from PyQt5.QtCore import QSettings

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.layout = QVBoxLayout(self)
        
        # Theme selection
        theme_layout = QHBoxLayout()
        theme_layout.addWidget(QLabel("Theme:"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark"])
        theme_layout.addWidget(self.theme_combo)
        self.layout.addLayout(theme_layout)
        
        # Default folder depth
        depth_layout = QHBoxLayout()
        depth_layout.addWidget(QLabel("Default Folder Depth:"))
        self.depth_combo = QComboBox()
        self.depth_combo.addItems([str(i) for i in range(1, 11)])
        depth_layout.addWidget(self.depth_combo)
        self.layout.addLayout(depth_layout)
        
        # Auto-check for updates
        self.auto_update_check = QCheckBox("Automatically check for updates")
        self.layout.addWidget(self.auto_update_check)
        
        # Save and Cancel buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_settings)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        self.layout.addLayout(button_layout)
        
        self.load_settings()
    
        # Load saved settings
    def load_settings(self):
        settings = QSettings("darkstarworks", "LLM-Coding Toolset")
        self.theme_combo.setCurrentText(settings.value("theme", "Light"))
        self.depth_combo.setCurrentText(settings.value("default_depth", "3"))
        self.auto_update_check.setChecked(settings.value("auto_update", True, type=bool))
    
        # Save current settings
    def save_settings(self):
        settings = QSettings("darkstarworks", "LLM-Coding Toolset")
        settings.setValue("theme", self.theme_combo.currentText())
        settings.setValue("default_depth", self.depth_combo.currentText())
        settings.setValue("auto_update", self.auto_update_check.isChecked())
        self.accept()