import unittest
from PyQt6 import QtWidgets, QtCore

import sys
from io import StringIO
import os


# Add the directory containing 'main.py' to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import Ui_MainWindow

class TestMainWindow(unittest.TestCase):
    def setUp(self):
        """Set up the application and the main window."""
        self.app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.MainWindow.show()

    def test_button_click(self):
        """Test if button click prints 'hello'."""
        button = self.ui.pushButton

        # Redirect stdout to capture print statements
        captured_output = StringIO()
        sys.stdout = captured_output

        # Simulate button click
        button.clicked.emit()

        # Restore stdout
        sys.stdout = sys.__stdout__

        # Check the output
        self.assertIn('hello', captured_output.getvalue())

    def tearDown(self):
        """Clean up the application."""
        self.app.quit()

if __name__ == '__main__':
    unittest.main()
