import unittest
import pandas as pd
from unittest.mock import MagicMock
from Shared_B_AdhocTracker_Logic_Page import AdhocTrackerButtonFunctionality
import datetime as datetime
import Shared_B_Credentials_Logic_Page as Shared_B_Credentials_Logic_Page

class TestAdhocTrackerFunctionality(unittest.TestCase):

    def test_process_input_data_with_valid_text(self):
        """Test process_input_data with a valid text input."""
        
        # Initialize the necessary test inputs
        sender_info_singlelocation = "U131234"
        link_singlelocation2 = '<a href="http://example.com">Example</a>'
        ValidityFrom_singlelocation = "12/12/2024"
        ValidityTo_singlelocation = "12/13/2024"
        airlineselection = '4O - Interjet'
        cscselection = 'BUR 1382'
        projectmessage = "Test message"
        priorityselection = 'Low'

        # Create a mock message object with a 'close' method
        msg = MagicMock()
        msg.close = MagicMock()

        # Call the process_input_data function
        result = AdhocTrackerButtonFunctionality.SingleLocation_Submit_button_logic(
            sender_info_singlelocation, link_singlelocation2, 
            ValidityFrom_singlelocation, ValidityTo_singlelocation, 
            airlineselection, cscselection, projectmessage, 
            priorityselection, msg  # Pass the mock msg object
        )

        # Define expected output
        currentprojects_data = {
            'current_department': 'Data Management',
            'current_analyst': 'Unassigned',
        }
        expected_output = pd.DataFrame([currentprojects_data])
        print(expected_output)
        
        # Check if the returned dataframe is as expected
        pd.testing.assert_frame_equal(result, expected_output)

# Run the test
if __name__ == "__main__":
    unittest.main()
