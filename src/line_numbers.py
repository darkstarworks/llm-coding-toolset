from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
                             QPushButton, QPlainTextEdit, QLabel, QFileDialog, QSpinBox)
from PyQt5.QtGui import QFont
import pyperclip

class LineNumbersTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        # File input
        file_layout = QHBoxLayout()
        self.file_input = QLineEdit()
        self.file_browse_button = QPushButton("Browse")
        self.file_browse_button.clicked.connect(self.browse_file)
        file_layout.addWidget(self.file_input)
        file_layout.addWidget(self.file_browse_button)
        self.layout.addLayout(file_layout)

        # Code input
        self.code_input = QPlainTextEdit()
        self.code_input.setFont(QFont("Courier", 10))
        self.layout.addWidget(self.code_input)

        # Options
        options_layout = QHBoxLayout()
        self.start_line = QSpinBox()
        self.start_line.setMinimum(1)
        options_layout.addWidget(QLabel("Start Line:"))
        options_layout.addWidget(self.start_line)
        self.layout.addLayout(options_layout)

        # Add line numbers button
        self.add_numbers_button = QPushButton("Add Line Numbers")
        self.add_numbers_button.clicked.connect(self.add_line_numbers)
        self.layout.addWidget(self.add_numbers_button)

        # Output
        self.output = QPlainTextEdit()
        self.output.setFont(QFont("Courier", 10))
        self.output.setReadOnly(True)
        self.layout.addWidget(self.output)

        # Copy to clipboard button
        self.copy_button = QPushButton("Copy to Clipboard")
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        self.layout.addWidget(self.copy_button)

    def browse_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select File")
        if file:
            self.file_input.setText(file)
            self.start_line.setEnabled(False)
            self.start_line.setToolTip("To manually set start line, please remove the added file")
            with open(file, 'r') as f:
                self.file_contents = f.read()

    def find_lines_for_snippet(self, snippet):
        file_lines = self.file_contents.splitlines()
        snippet_lines = snippet.splitlines()
        start = -1

        for i in range(len(file_lines) - len(snippet_lines) + 1):
            if all(file_lines[i+j].lstrip().startswith(snippet_line.lstrip()) for j, snippet_line in enumerate(snippet_lines)):
                start = i + 1  # Line numbers start at 1
                break
        return start

    def add_line_numbers(self):
        snippet = self.code_input.toPlainText()
        if not snippet:
            return

        # If file is loaded, find the start line of the snippet
        if hasattr(self, 'file_contents'):
            start = self.find_lines_for_snippet(snippet)
            if start != -1:
                self.start_line.setValue(start)
            else:
                self.output.setPlainText("Snippet not found in the loaded file.")
                return
        else:
            start = self.start_line.value()

        # Calculate the width of the line number column based on the highest line number
        num_lines = len(snippet.splitlines())
        max_line_number = start + num_lines - 1
        line_number_width = len(str(max_line_number))

        # Generate the output with correctly aligned line numbers
        output = []
        for i, line in enumerate(snippet.splitlines(), start=start):
            formatted_line_number = f"{i:>{line_number_width}}"
            output.append(f"{formatted_line_number}: {line}")

        self.output.setPlainText("\n".join(output))

    def copy_to_clipboard(self):
        pyperclip.copy(self.output.toPlainText())