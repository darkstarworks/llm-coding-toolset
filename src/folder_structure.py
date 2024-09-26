# folder_structure.py
# This module provides a tab for visualizing and exporting folder structures.

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
                             QPushButton, QTreeWidget, QTreeWidgetItem, QCheckBox, 
                             QLabel, QFileDialog, QComboBox)
from PyQt5.QtCore import Qt
import os
import pyperclip

class FolderStructureTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        # Folder selection
        folder_layout = QHBoxLayout()
        self.folder_input = QLineEdit()
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_folder)
        folder_layout.addWidget(self.folder_input)
        folder_layout.addWidget(self.browse_button)
        self.layout.addLayout(folder_layout)

        # Depth selection
        depth_layout = QHBoxLayout()
        depth_layout.addWidget(QLabel("Depth:"))
        self.depth_combo = QComboBox()
        self.depth_combo.addItems([str(i) for i in range(1, 11)])
        depth_layout.addWidget(self.depth_combo)
        self.view_button = QPushButton("View")
        self.view_button.clicked.connect(self.view_structure)
        depth_layout.addWidget(self.view_button)
        self.layout.addLayout(depth_layout)

        # Tree view
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Name", "Size"])
        self.tree.itemChanged.connect(self.on_item_changed)
        self.layout.addWidget(self.tree)

        # Options
        self.include_contents = QCheckBox("Include file contents")
        self.layout.addWidget(self.include_contents)

        # Info labels
        self.line_count_label = QLabel("Total lines: 0")
        self.file_size_label = QLabel("Total size: 0 bytes")
        self.layout.addWidget(self.line_count_label)
        self.layout.addWidget(self.file_size_label)

        # Generate button
        self.generate_button = QPushButton("Generate and Copy to Clipboard")
        self.generate_button.clicked.connect(self.generate_output)
        self.layout.addWidget(self.generate_button)

        # Open a file dialog to select a folder
    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folder_input.setText(folder)

        # Display the folder structure in the tree view
    def view_structure(self):
        self.tree.clear()
        folder = self.folder_input.text()
        depth = int(self.depth_combo.currentText())

        if not os.path.isdir(folder):
            return

        root = QTreeWidgetItem(self.tree, [folder])
        root.setFlags(root.flags() | Qt.ItemIsUserCheckable)
        root.setCheckState(0, Qt.Checked)
        self.add_tree_items(root, folder, depth)
        self.tree.expandAll()
        self.update_info()

        # Recursively add items to the tree view
    def add_tree_items(self, parent, path, depth):
        if depth == 0:
            return

        for name in os.listdir(path):
            full_path = os.path.join(path, name)
            size = os.path.getsize(full_path)
            item = QTreeWidgetItem(parent, [name, f"{size} bytes"])
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(0, Qt.Checked)

            if os.path.isdir(full_path):
                self.add_tree_items(item, full_path, depth - 1)

        # Handle changes in item selection
    def on_item_changed(self, item, column):
        if column == 0:
            new_state = item.checkState(0)
            self.update_children(item, new_state)
            self.update_parents(item.parent())
        self.update_info()

        # Update the check state of child items
    def update_children(self, item, check_state):
        for i in range(item.childCount()):
            child = item.child(i)
            child.setCheckState(0, check_state)
            self.update_children(child, check_state)

        # Update the check state of parent items
    def update_parents(self, item):
        if item is None:
            return

        checked_count = sum(item.child(i).checkState(0) == Qt.Checked for i in range(item.childCount()))
        total_count = item.childCount()

        if checked_count == 0:
            item.setCheckState(0, Qt.Unchecked)
        elif checked_count == total_count:
            item.setCheckState(0, Qt.Checked)
        else:
            item.setCheckState(0, Qt.PartiallyChecked)

        self.update_parents(item.parent())

        # Update the total lines and size information
    def update_info(self):
        total_lines = 0
        total_size = 0

        def count_lines_and_size(item):
            nonlocal total_lines, total_size
            if item.checkState(0) == Qt.Checked:
                path = self.get_full_path(item)
                if os.path.isfile(path):
                    size = int(item.text(1).split()[0])
                    total_size += size
                    if self.include_contents.isChecked():
                        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                            total_lines += sum(1 for _ in f)
                for i in range(item.childCount()):
                    count_lines_and_size(item.child(i))

        root = self.tree.invisibleRootItem()
        for i in range(root.childCount()):
            count_lines_and_size(root.child(i))

        self.line_count_label.setText(f"Total lines: {total_lines}")
        self.file_size_label.setText(f"Total size: {total_size} bytes")

        # Get the full path of an item in the tree
    def get_full_path(self, item):
        path = item.text(0)
        parent = item.parent()
        while parent:
            path = os.path.join(parent.text(0), path)
            parent = parent.parent()
        return path

        # Generate and copy the folder structure to clipboard
    def generate_output(self):
        output = []

        def generate_structure(item, level=0):
            if item.checkState(0) == Qt.Checked:
                path = self.get_full_path(item)
                output.append("  " * level + item.text(0))
                if os.path.isfile(path) and self.include_contents.isChecked():
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        output.append("  " * (level + 1) + "Content:")
                        output.extend("  " * (level + 2) + line for line in content.splitlines())
                for i in range(item.childCount()):
                    generate_structure(item.child(i), level + 1)

        root = self.tree.invisibleRootItem()
        for i in range(root.childCount()):
            generate_structure(root.child(i))

        pyperclip.copy("\n".join(output))