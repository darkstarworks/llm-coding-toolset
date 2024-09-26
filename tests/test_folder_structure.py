# From the root directory, run:
# python -m unittest tests.test_folder_structure

import unittest
from PyQt5.QtWidgets import QApplication, QTreeWidgetItem
from src.folder_structure import FolderStructureTab
import os
import tempfile
import shutil

class TestFolderStructure(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    def setUp(self):
        self.folder_structure_tab = FolderStructureTab()
        # Create a temporary directory structure for testing
        self.test_dir = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.test_dir, "subfolder"))
        with open(os.path.join(self.test_dir, "file1.txt"), "w") as f:
            f.write("Test content")
        with open(os.path.join(self.test_dir, "subfolder", "file2.txt"), "w") as f:
            f.write("Subfolder content")

    def tearDown(self):
        # Clean up the temporary directory after each test
        shutil.rmtree(self.test_dir)

    def test_add_tree_items(self):
        root = QTreeWidgetItem(self.folder_structure_tab.tree)
        root.setText(0, self.test_dir)
        self.folder_structure_tab.add_tree_items(root, self.test_dir, 2)
        
        # Check if the root item has the correct number of children
        self.assertEqual(root.childCount(), 2)  # 1 file and 1 subfolder
        
        # Check if the subfolder is correctly added
        subfolder = root.child(0) if root.child(0).text(0) == "subfolder" else root.child(1)
        self.assertEqual(subfolder.text(0), "subfolder")
        self.assertEqual(subfolder.childCount(), 1)  # 1 file in subfolder
        
        # Check if the file in the subfolder is correctly added
        subfile = subfolder.child(0)
        self.assertEqual(subfile.text(0), "file2.txt")

    # ... (other test methods)

if __name__ == '__main__':
    unittest.main()