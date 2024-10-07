# tests/test_main.py

import pytest
from unittest.mock import MagicMock
from main import Ui_MainWindow
import pandas as pd
from PyQt6 import QtCore

def test_display_dataframe():
    # Create a mock for QLabel
    mock_label = MagicMock()
    
    # Create an instance of Ui_MainWindow
    ui = Ui_MainWindow()
    
    # Assign the mock label to the ui
    ui.label = mock_label
    
    # Call the display_dataframe method
    ui.display_dataframe()
    
    # Define the expected DataFrame and its HTML representation
    data = {
        "Name": ["Bro", "Bob", "Charlie", "Diana"],
        "Age": [25, 30, 35, 28],
        "Department": ["HR", "Engineering", "Marketing", "Design"],
        "Salary": [50000, 70000, 60000, 65000]
    }
    df = pd.DataFrame(data)
    expected_html = df.to_html(index=False)
    
    # Check that setText was called with expected_html
    mock_label.setText.assert_called_with(expected_html)
    
    # Check that setTextFormat was called with RichText
    mock_label.setTextFormat.assert_called_with(QtCore.Qt.TextFormat.RichText)
