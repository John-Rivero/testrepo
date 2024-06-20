import unittest
from PyQt6 import QtWidgets
from main import Ui_MainWindow
import sys
from io import StringIO

class TestMainWindow(unittest.TestCase):
    def setUp(self):
        """Set up the application and the main window."""
        self.app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.MainWindow.show()

    def test_button_click(self):
        """Test if button click prints 'hello', 'test', and 'This is second test'."""
        button = self.ui.pushButton

        # Redirect stdout to capture print statements
        captured_output = StringIO()
        sys.stdout = captured_output

        # Simulate button click
        button.clicked.emit()

        # Restore stdout
        sys.stdout = sys.__stdout__

        # Check the output
        output = captured_output.getvalue()
        self.assertIn('hello', output)
        self.assertIn('test', output)
        self.assertIn('This is second test', output)

    def tearDown(self):
        """Clean up the application."""
        self.app.quit()

if __name__ == '__main__':
    unittest.main()
