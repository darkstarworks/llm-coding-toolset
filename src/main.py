# main.py
# LLM-Coding Toolset
# 
# This application provides a set of tools to assist developers working with Large Language Models (LLMs).
# It includes features for visualizing folder structures, adding line numbers to code snippets,
# and comparing text differences.

import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, QAction, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSettings
from src.folder_structure import FolderStructureTab
from src.line_numbers import LineNumbersTab
from src.diff_viewer import DiffViewerTab
from src.settings import SettingsDialog
from src.update_checker import check_for_updates

os.environ['QT_ENABLE_HIGHDPI_SCALING'] = '0'
os.environ['QT_FONT_DPI'] = '96'

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LLM-Coding Tools")
        self.setGeometry(100, 100, 800, 600)
        
        # Adding an icon
        icon_path = os.path.join(os.path.dirname(__file__), '..', 'resources', 'icon.png')
        self.setWindowIcon(QIcon(icon_path))

        # Set up the central widget and main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        # Create and set up the tab widget
        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        # Initialize the three main tool tabs
        self.folder_structure_tab = FolderStructureTab()
        self.line_numbers_tab = LineNumbersTab()
        self.diff_viewer_tab = DiffViewerTab()

        # Add the tool tabs to the tab widget
        self.tabs.addTab(self.folder_structure_tab, "Folder Structure")
        self.tabs.addTab(self.line_numbers_tab, "Add Line Numbers")
        self.tabs.addTab(self.diff_viewer_tab, "Diff Viewer")

        self.create_menu()
        self.load_settings()

    def create_menu(self):
        # Create the main menu bar with File and Help menus
        menu_bar = self.menuBar()
        
        # File menu
        file_menu = menu_bar.addMenu("File")
        
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.open_settings)
        file_menu.addAction(settings_action)
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Help menu
        help_menu = menu_bar.addMenu("Help")
        
        update_action = QAction("Check for Updates", self)
        update_action.triggered.connect(self.check_updates)
        help_menu.addAction(update_action)
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def open_settings(self):
        # Open the settings dialog
        dialog = SettingsDialog(self)
        if dialog.exec_():
            self.load_settings()

    def load_settings(self):
        # Load and apply user settings
        settings = QSettings("darkstarworks", "LLM-Coding Toolset")
        theme = settings.value("theme", "Light")
        self.apply_theme(theme)
        
        # Set the default folder structure depth
        default_depth = int(settings.value("default_depth", 3))
        self.folder_structure_tab.depth_combo.setCurrentText(str(default_depth))

    def apply_theme(self, theme):
        # Apply the selected theme (light or dark)
        # TODO: Implement theme application logic
        pass

    def check_updates(self):
        # Check for available updates
        check_for_updates(self)

    def show_about(self):
        # Display information about the application
        QMessageBox.about(self, "About LLM-Coding Toolset", 
                          "LLM-Coding Toolset v1.0.0\n\n"
                          "A set of tools to assist developers working with Large Language Models.")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()