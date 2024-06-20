import unittest
import sys
import os
from PyQt6 import QtWidgets
# Add the directory containing 'main.py' to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import main

class TestMainWindow(unittest.TestCase):
    def setUp(self):
        self.app = QtWidgets.QApplication([])
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = main.Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)

    def test_pushButton_text(self):
        self.assertEqual(self.ui.pushButton.text(), "PushButton")

    def test_pushButton_click(self):
        with self.assertLogs(level='INFO') as log:
            self.ui.pushButton.click()
            self.assertIn('hello', log.output[0])

if __name__ == '__main__':
    unittest.main()
