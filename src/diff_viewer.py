# diff_viewer.py
# This module provides a tab for comparing and visualizing differences between two texts.

import difflib
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, 
                             QPushButton, QScrollArea, QFileDialog)
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt, QRect, QSize

class DiffViewerTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        # Create text inputs
        self.text1 = QTextEdit()
        self.text2 = QTextEdit()

        # Create buttons
        self.load_file1_button = QPushButton("Load File 1")
        self.load_file2_button = QPushButton("Load File 2")
        self.compare_button = QPushButton("Compare")

        # Connect buttons to functions
        self.load_file1_button.clicked.connect(lambda: self.load_file(1))
        self.load_file2_button.clicked.connect(lambda: self.load_file(2))
        self.compare_button.clicked.connect(self.compare_texts)

        # Create layout for inputs and buttons
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.text1)
        input_layout.addWidget(self.text2)
        self.layout.addLayout(input_layout)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.load_file1_button)
        button_layout.addWidget(self.load_file2_button)
        button_layout.addWidget(self.compare_button)
        self.layout.addLayout(button_layout)

        # Create diff viewer
        self.diff_viewer = DiffViewer()
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.diff_viewer)
        scroll_area.setWidgetResizable(True)
        self.layout.addWidget(scroll_area)

    def load_file(self, text_box_number):
        file_path, _ = QFileDialog.getOpenFileName(self, f"Select File for Text {text_box_number}")
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                if text_box_number == 1:
                    self.text1.setPlainText(content)
                else:
                    self.text2.setPlainText(content)

    def compare_texts(self):
        text1 = self.text1.toPlainText().splitlines()
        text2 = self.text2.toPlainText().splitlines()
        diff = list(difflib.unified_diff(text1, text2, lineterm='', n=0))
        self.diff_viewer.set_diff(diff)

class DiffViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.diff_lines = []

        # Set the diff content to be displayed
    def set_diff(self, diff):
        self.diff_lines = diff[2:]  # Skip the first two lines (metadata)
        self.update()

        # Custom paint event to render the diff view
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        font = painter.font()
        font.setFamily("Courier")
        painter.setFont(font)

        y = 5
        line_height = painter.fontMetrics().height()

        for line in self.diff_lines:
            if line.startswith('+'):
                painter.fillRect(0, y, self.width(), line_height, QColor(230, 255, 237))
                painter.setPen(QColor(46, 160, 67))
            elif line.startswith('-'):
                painter.fillRect(0, y, self.width(), line_height, QColor(255, 238, 240))
                painter.setPen(QColor(215, 58, 73))
            else:
                painter.setPen(Qt.black)

            painter.drawText(5, y + line_height - 2, line)
            y += line_height

        self.setMinimumHeight(y)

        # Provide a default size hint for the widget
    def sizeHint(self):
        return QSize(600, len(self.diff_lines) * 20)