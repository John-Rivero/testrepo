from PyQt6 import QtCore, QtGui, QtWidgets
import pandas as pd

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 300)  # Increased size to accommodate QLabel
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # Push Button
        self.pushButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(50, 20, 300, 50))  # Adjusted size and position
        self.pushButton.setObjectName("pushButton")
        
        # Label to display DataFrame
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 80, 300, 200))  # Positioned below the button
        self.label.setObjectName("label")
        self.label.setWordWrap(True)  # Enable word wrapping for better readability
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 400, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Connect the button click to the display_dataframe function
        self.pushButton.clicked.connect(self.display_dataframe)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "DataFrame Display"))
        self.pushButton.setText(_translate("MainWindow", "Show DataFrame"))
        self.label.setText(_translate("MainWindow", "DataFrame will appear here."))

    def display_dataframe(self):
        # Create a sample DataFrame
        data = {
            "Name": ["Bro", "Bob", "Charlie", "Diana"],
            "Age": [25, 30, 35, 28],
            "Department": ["HR", "Engineering", "Marketing", "Design"],
            "Salary": [50000, 70000, 60000, 65000]
        }
        df = pd.DataFrame(data)
        
        # Convert DataFrame to HTML for better formatting
        df_html = df.to_html(index=False)
        
        # Option 1: Display as plain text
        # self.label.setText(df.to_string(index=False))
        
        # Option 2: Display as HTML (better formatting)
        self.label.setText(df_html)
        
        # Optional: Enable rich text to render HTML properly
        self.label.setTextFormat(QtCore.Qt.TextFormat.RichText)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
