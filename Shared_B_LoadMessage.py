#This is mainly for displaying loading message


from PyQt6.QtWidgets import  QApplication,  QProgressDialog, QWidget, QMessageBox
from PyQt6.QtCore import Qt
        
def show_message1(self):
    try:
        parent = self if isinstance(self, QWidget) else None

        self.msg = QProgressDialog(parent=parent)
        self.msg.setLabelText("File loading, please wait a moment")
        self.msg.setWindowTitle("Information")
        self.msg.setWindowModality(Qt.WindowModality.WindowModal)
        self.msg.setCancelButton(None)
        self.msg.setMinimumDuration(0)
        self.msg.setRange(0, 0)  # This will hide the progress bar
        self.msg.setStyleSheet("QProgressBar {border: 0px; height: 0px; margin: 0px; padding: 0px;}")  # Hide the progress bar
        self.msg.show()
        QApplication.processEvents()
        return self.msg

    except Exception as error:
            QMessageBox.critical(None, "Error", str(error), QMessageBox.StandardButton.Ok)
            return 
        
        
def show_message2(self):
    try:
        parent = self if isinstance(self, QWidget) else None

        self.msg = QProgressDialog(parent=parent)
        self.msg.setLabelText("Processing, please wait a moment")
        self.msg.setWindowTitle("Information")
        self.msg.setWindowModality(Qt.WindowModality.WindowModal)
        self.msg.setCancelButton(None)
        self.msg.setMinimumDuration(0)
        self.msg.setRange(0, 0)  # This will hide the progress bar
        self.msg.setStyleSheet("QProgressBar {border: 0px; height: 0px; margin: 0px; padding: 0px;}")  # Hide the progress bar
        self.msg.show()
        QApplication.processEvents()
        return self.msg

    except Exception as error:
            QMessageBox.critical(None, "Error", str(error), QMessageBox.StandardButton.Ok)
            return 