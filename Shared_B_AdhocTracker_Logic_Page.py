from PyQt6.QtWidgets import  QFileDialog, QMessageBox
from bs4 import BeautifulSoup
 
import pandas as pd, sqlite3, os, shutil, random, datetime
import Shared_B_Credentials_Logic_Page as Shared_B_Credentials_Logic_Page 
import Shared_B_AirlineCode as Data_B_AirlineCode


class AdhocTrackerButtonFunctionality:
    
    #Path for the current projects
    directory_path = r"M:\LSGN\ARHD38-LSGN1\everyone\Analytica\Z)AnalyticaDataBase\AdhocTracker\AdhocTracker_CurrentProjects\AllProjects"
     
    #AdhocDatabase - Table
    csc_table_name =                'csc_table'
    currentproject_table_name =     'current_projects'
    adhoc_messages_table_name =     'adhoc_messages'
    
    #UserDatabase - Table
    users_table =                   'users'
    
    #targetfolder location
    targetfolder =                  r'textfiles\AdhocTracker'

#################################################################################################################################################
#################################################################################################################################################
    #REPEATED STEPS
    

    @staticmethod
    def connectAdhocDatabase(): #ADHOC TRACKER DATABASE
        try:
            #Use this for Prod
            database_adhoc_tracker_path = r"M:\LSGN\ARHD38-LSGN1\everyone\Analytica\Z)AnalyticaDataBase\AdhocTracker"
            #adhocproject_database = 'AdhocTrackerMain.db'
            adhocproject_database = 'AdhocTrackerTest.db'
            
        
            
            database_path = os.path.join(database_adhoc_tracker_path, adhocproject_database)
            return database_path
    
        except Exception as error:
            QMessageBox.critical(None, "Error", str(error), QMessageBox.StandardButton.Ok)
            return   

    @staticmethod
    def connectUserDatabase(): #USER DATABASE
        try:
            #name of the database / name of the table
            database_user_path = r'M:\LSGN\ARHD38-LSGN1\everyone\Analytica\Z)AnalyticaDataBase\Users'
            user_database = "UsersDB.db"
            database_path2 = os.path.join(database_user_path, user_database)
            return database_path2

        except Exception as error:
            QMessageBox.critical(None, "Error", str(error), QMessageBox.StandardButton.Ok)
            return   


    @staticmethod
    def create_projects_folder(current_project_folder_name): #THIS FUNCTION IS FOR CREATING A PROJECT FOLDER WHERE ALL ATTACHED FILES ARE BEING LOADED TO
        try:
            #JOIN the file for both directory path and the name of the csv file
            projectfolder_path = os.path.join(AdhocTrackerButtonFunctionality.directory_path, current_project_folder_name)
            try:
                os.makedirs(projectfolder_path, exist_ok=True)
                pass
            except OSError as error:
                pass        
            
            
            #CREATE THE UPLOAD FOLDER(This is where the attached files are going to be stored into)--------------------------------
            upload_folder_name = f'UploadFolder'
            
            #JOIN the file for both directory path and the name of the csv file
            projectfolder_path2 = os.path.join(projectfolder_path, upload_folder_name)
            try:
                os.makedirs(projectfolder_path2, exist_ok=True)
                pass
            except OSError as error:
                pass
            
            #TRANSFER THE CONTENTS OF targetfolder TO projectfolder_path-------------------------------------------------------------------------
            AdhocTrackerButtonFunctionality.move_contents(AdhocTrackerButtonFunctionality.targetfolder, projectfolder_path2)  
        
        except Exception as error:
            QMessageBox.critical(None, "Error", str(error), QMessageBox.StandardButton.Ok)
            return   

    @staticmethod
    def SingleLocation_Submit_button_logic(sender_info_singlelocation, link_singlelocation2, ValidityFrom_singlelocation, ValidityTo_singlelocation, airlineselection, cscselection, projectmessage, priorityselection, msg):  # THIS FUNCTION IS FOR SINGLELOCATION SUBMISSION
        try:
            # Retrieve the current date
            current_date = str(datetime.datetime.now())

            # Generate a unique ID based on the date and time
            designated_id = current_date[:16].replace("-", ".").replace(" ", "--").replace(":", ".")

            # Retrieve user info and validate credentials
            sender_info_singlelocation = sender_info_singlelocation
            sender_info_singlelocation2 = Shared_B_Credentials_Logic_Page.data[sender_info_singlelocation]
            sender_info_singlelocation3 = f'{sender_info_singlelocation} - {sender_info_singlelocation2}'

            # Retrieve the attached link
            link_singlelocation2 = link_singlelocation2
            soup = BeautifulSoup(link_singlelocation2, 'lxml')
            link_singlelocation2 = soup.find('a')['href'] if soup.find('a') else "No link attached"

            # Retrieve Validity From and To dates
            ValidityFrom_singlelocation = ValidityFrom_singlelocation
            ValidityTo_singlelocation = ValidityTo_singlelocation

            # Retrieve Airline Info
            airlineselection = airlineselection
            if airlineselection == "Select an Airline":
                QMessageBox.critical(None, "Error", "Please select a valid airline.", QMessageBox.StandardButton.Ok)
                msg.close()
                return

            cscselection = cscselection
            if cscselection == "Select a CSC":
                QMessageBox.critical(None, "Error", "Please select a valid CSC.", QMessageBox.StandardButton.Ok)
                msg.close()
                return

            # Retrieve message and priority
            projectmessage = projectmessage
            priorityselection = priorityselection

            # Create the project folder
            current_project_folder_name = f'{airlineselection}-{cscselection} -- {designated_id}'
            AdhocTrackerButtonFunctionality.create_projects_folder(current_project_folder_name)

            ##########################################################################################################################################
            # Insert data into the database tables

            # Data for csc_table
            csc_table_data = {
                "project_name": current_project_folder_name,
                "project_id": designated_id,
                "sender": sender_info_singlelocation3,
                "hyperlink": link_singlelocation2,
                "validity_from": ValidityFrom_singlelocation,
                "validity_to": ValidityTo_singlelocation,
                "airline": airlineselection,
                "csc1": cscselection,
                "message": projectmessage,
                "priority": priorityselection
            }
            csc_table_data_df = pd.DataFrame([csc_table_data])  # Wrap in list to create single-row DataFrame

            # Data for current_projects
            currentprojects_data = {
                "project_id": designated_id,
                "project_name": current_project_folder_name,
                'current_department': 'Data Management',
                'current_analyst': 'Unassigned',
                'status': '',
                'data_analyst': '',
                'data_project_started': '',
                'data_project_ended': '',
                'costing_to_data_rework_count': 0,
                'costing_analyst': '',
                'costing_project_started': '',
                'costing_project_ended': '',
                'pricing_to_costing_rework_count': 0,
                'pricing_analyst': '',
                'pricing_project_started': '',
                'pricing_project_ended': '',
                'priority': priorityselection
            }
            currentprojects_df = pd.DataFrame([currentprojects_data])  # Wrap in list to create single-row DataFrame

            #INSERT INTO THE DATABASE-------------------------------------------------------------------------------------------
            conn = sqlite3.connect(AdhocTrackerButtonFunctionality.connectAdhocDatabase())
            
            csc_table_data_df.to_sql(AdhocTrackerButtonFunctionality.csc_table_name, conn, if_exists='append', index=False)
            currentprojects_df.to_sql(AdhocTrackerButtonFunctionality.currentproject_table_name, conn, if_exists='append', index=False)
            
            conn.commit()             
            conn.close()
            

            ##########################################################################################################################################
            # Retrieve target user information from the database

            #This is to retrieve the target users info
            conn1 = sqlite3.connect(AdhocTrackerButtonFunctionality.connectUserDatabase())
            
            users_managers_df = pd.read_sql('SELECT * FROM users', conn1)
            users_managers_df = users_managers_df[(users_managers_df['department'] == 'Data') & (users_managers_df['position'] == 'Manager')]
            users_managers_df = users_managers_df['user_id'].tolist()
            
            conn1.close()

            ##########################################################################################################################################
            # Insert messages into the adhoc_messages table for each manager

            conn2 = sqlite3.connect(AdhocTrackerButtonFunctionality.connectAdhocDatabase())

            for users_managers_df2 in users_managers_df:
                #Insert a message into adhoc_messages
                adhocmessages_data = {
                            "project_name" :                            [current_project_folder_name],
                            "sender" :                                  [sender_info_singlelocation3],
                            'message_sent_timestamp' :                  [current_date],
                            'message_text' :                            [f'A new project has been created'],
                            'message_status' :                          ['Unread'],
                            'receiver' :                                [users_managers_df2],
                            'message_read_timestamp' :                  ['']
                        }
                adhocmessages_df = pd.DataFrame(adhocmessages_data)    
                adhocmessages_df.to_sql(AdhocTrackerButtonFunctionality.adhoc_messages_table_name, conn2, if_exists='append', index=False)        
            
            conn2.commit()
            conn2.close()

            ##########################################################################################################################################
            #THE WHOLE SECTION BELOW IS FOR CLEANUP
                        
            #REMOVE any contents of the targetfolder
            for filename in os.listdir(AdhocTrackerButtonFunctionality.targetfolder):
                file_path2 = os.path.join(AdhocTrackerButtonFunctionality.targetfolder, filename)
                
                try:
                    # Check if it's a file or a directory
                    if os.path.isfile(file_path2) or os.path.islink(file_path2):
                        os.unlink(file_path2)  # Remove the file or link
                
                except Exception as error:
                    QMessageBox.critical(None, "Error", str(error), QMessageBox.StandardButton.Ok)
                    msg.close()
                    return  
                
                
            #Clear all the input fields within the App
            QMessageBox.information(None, "Success", f"Project has been created", QMessageBox.StandardButton.Ok)
            msg.close()
            
            
            
            ###################################################################################################################################
            #############################################################################################################################################
            #THIS DISPLAYS TO THE CURRENT PROJECTS SECTION
            conn3 = sqlite3.connect(AdhocTrackerButtonFunctionality.connectAdhocDatabase())
            
            current_df = pd.read_sql('SELECT * FROM current_projects', conn3)
            current_df = current_df[['current_department', 'current_analyst']].fillna('')
            print (current_df)
            return current_df
                    
            
        except Exception as error:
            QMessageBox.critical(None, "Error", str(error), QMessageBox.StandardButton.Ok)
            msg.close()
            return



    def SingleLocation_Submit_button_Clicked(self, msg):
        sender_info_singlelocation = self.SingleLocation_SenderName_textbox.toPlainText()
        link_singlelocation2 = self.SingleLocation_AttachLink_textBrowser.toHtml()
        ValidityFrom_singlelocation = str(self.SingleLocation_ValidityFrom_textbox.toPlainText()) or "No 'From' Validity"
        ValidityTo_singlelocation = str(self.SingleLocation_ValidityTo_textbox.toPlainText()) or "No 'To' Validity"
        airlineselection = self.SingleLocation_Airline_comboBox.currentText()
        cscselection = self.SingleLocation_Airline_CSC_comboBox.currentText()
        projectmessage = self.AdhocTracker_CreateProject_Display.toPlainText()
        priorityselection = self.SingleLocation_Priority_comboBox.currentText()
        msg = msg
        
        
        AdhocTrackerButtonFunctionality.SingleLocation_Submit_button_logic(sender_info_singlelocation, link_singlelocation2, ValidityFrom_singlelocation, ValidityTo_singlelocation, airlineselection, cscselection, projectmessage, priorityselection, msg)


        self.SingleLocation_AttachLink_textBrowser.clear()
        self.SingleLocation_AttachFile_button.setText("Attach a file")
        self.AdhocTracker_CreateProject_Display.clear()
        self.SingleLocation_AttachFile_button.setStyleSheet("QPushButton{color: rgb(0, 0, 0);border : 1px solid  rgb(100, 100, 100);padding-left: 20px;padding-right: 20px;border-radius: 4px;background-color: rgb(255,255,255);}")
        self.SingleLocation_ValidityFrom_textbox.clear()
        self.SingleLocation_ValidityTo_textbox.clear()
        self.SingleLocation_Airline_comboBox.setCurrentIndex(0)
        self.SingleLocation_Airline_CSC_comboBox.setCurrentIndex(0)
        self.SingleLocation_Priority_comboBox.setCurrentIndex(0)

    def provide_department_name(self):  #THIS FUNCTION RETRIEVES THE USER'S DEPARTMENT
        try:
            with open(r"textfiles\Shared\department_name.txt", "r") as file:
                dept = file.read()
            return dept
        
        except Exception as error:
            QMessageBox.critical(None, "Error", str(error), QMessageBox.StandardButton.Ok)
            return   

    
    def provide_analyst_name(self): #THIS FUNCTION RETRIEVES THE USER'S U#
        try:
            with open("textfiles/userID.txt", 'r') as analyst_u:
                    
                #this is the U# that is read when logging in
                analyst_u = analyst_u.read()
                analyst_name = Shared_B_Credentials_Logic_Page.data[analyst_u]
                
                #The output looks like this U123456 - John Doe
                fullinfo = f'{analyst_u} - {analyst_name}'
                return fullinfo
            
        except Exception as error:
            QMessageBox.critical(None, "Error", str(error), QMessageBox.StandardButton.Ok)
            return   

   
    def howmanyrows():  #THIS FUNCTION COUNTS HOW MANY ROWS ARE IN THE listcurrentprojects AND THEN USES THAT VALUE AS THE PROJECT ID
        try:
            # useridpath = "textfiles/userID.txt"
            # with open(useridpath, 'r') as userid:
            #     useridv = userid.read()
            
            randomvalue = random.randint(0, 99999)
            randomvalue2 = random.randint(0, 9999)
            
            randomgeneratedid = f'{randomvalue}.{randomvalue2}'
            
            return randomgeneratedid
    
        except Exception as error:
            QMessageBox.critical(None, "Error", str(error), QMessageBox.StandardButton.Ok)
            return   
    
  
    def move_contents(source_folder, destination_folder):   #THIS FUNCTION MOVES THE UPLOADED ATTACHED FILE TO THE DATABASE
        try:
            # Ensure the destination folder exists
            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)
            
            # Move all contents from source_folder to destination_folder
            for item in os.listdir(source_folder):
                source_path = os.path.join(source_folder, item)
                destination_path = os.path.join(destination_folder, item)
                
                # Check if it is a file or a directory
                if os.path.isdir(source_path):
                    shutil.move(source_path, destination_path)
                else:
                    shutil.move(source_path, destination_path)

        except Exception as error:
            QMessageBox.critical(None, "Error", str(error), QMessageBox.StandardButton.Ok)
            return   


    def create_projects_folder(current_project_folder_name): #THIS FUNCTION IS FOR CREATING A PROJECT FOLDER WHERE ALL ATTACHED FILES ARE BEING LOADED TO
        try:
            #JOIN the file for both directory path and the name of the csv file
            projectfolder_path = os.path.join(AdhocTrackerButtonFunctionality.directory_path, current_project_folder_name)
            try:
                os.makedirs(projectfolder_path, exist_ok=True)
                pass
            except OSError as error:
                pass        
            
            
            #CREATE THE UPLOAD FOLDER(This is where the attached files are going to be stored into)--------------------------------
            upload_folder_name = f'UploadFolder'
            
            #JOIN the file for both directory path and the name of the csv file
            projectfolder_path2 = os.path.join(projectfolder_path, upload_folder_name)
            try:
                os.makedirs(projectfolder_path2, exist_ok=True)
                pass
            except OSError as error:
                pass
            
            #TRANSFER THE CONTENTS OF targetfolder TO projectfolder_path-------------------------------------------------------------------------
            AdhocTrackerButtonFunctionality.move_contents(AdhocTrackerButtonFunctionality.targetfolder, projectfolder_path2)  
        
        except Exception as error:
            QMessageBox.critical(None, "Error", str(error), QMessageBox.StandardButton.Ok)
            return   


    def remove_folder_by_name(project_name):  #THIS FUNCTION IS FOR DELETING A PROJECT FOLDER WHERE ALL ATTACHED FILES ARE BEING LOADED TO
        try:
            for root, dirs, files in os.walk(AdhocTrackerButtonFunctionality.directory_path, topdown=False):
                for name in dirs:
                    folder_path = os.path.join(root, name)
                    if name == project_name:
                        
                        try:
                            shutil.rmtree(folder_path)
                            #print(f"Removed folder: {folder_path}")
                        
                        except Exception as e:
                            #print(f"Failed to remove {folder_path}. Reason: {e}")
                            return
                        
        except Exception as error:
            QMessageBox.critical(None, "Error", str(error), QMessageBox.StandardButton.Ok)
            return   


    def apply_html(dataframe): #THIS FUNCTION IS FOR CONVERTING A DATAFRAME INTO AN HTML
        try:
            html_table = dataframe.to_html(index=False, escape=False)
            table_style = """
                            <style>
                            table {
                                width: 100%;
                                border-collapse: collapse;
                                border-radius: 18px;
                                overflow: hidden;
                            }
                            th {
                                border 1px solid black;
                                background-color: rgb(80, 200, 200);
                                color: white;
                                font-weight: bold;
                                border-radius: 16px;
                                padding: 16px; /* Increased padding */
                                font-size: 12px; /* Increased font size */
                            }
                            td {
                                border 1px solid black;
                                padding: 10px; /* Increased padding */
                                font-size: 11px; /* Increased font size */
                            }
                            tr:nth-child(even) td {
                                background-color: rgb(0, 0, 0);
                            }
                            tr:nth-child(odd) td {
                                background-color: white;
                            }
                            </style>
                            """
            
            
            styled_html_table = f'{table_style}{html_table}'
            return styled_html_table
    
        except Exception as error:
            QMessageBox.critical(None, "Error", str(error), QMessageBox.StandardButton.Ok)
            return   



#################################################################################################################################################
#################################################################################################################################################
    #MAIN ADHOC TRACKER BUTTONS FUNCTIONALITIES


    # def SingleLocation_Submit_button_Clicked(self, msg): #THIS FUNCTION IS FOR SINGLELOCATION SUBMISSION   
    #     #try:
    #         ######################################################################################################################### 
    #         #RETRIEVE ALL INPUTS
    #         #retrieve the current date
    #         current_date = str(datetime.datetime.now())
            
    #         #Generate an ID      
    #         designated_id = current_date[:16].replace("-", ".").replace(" ", "--").replace(":", ".")
            

    #         #RETRIEVE THE USER INFO AND CHECK IF THE INFO MATCHES THE STORED CREDENTIALS
    #         # try:
    #         sender_info_singlelocation = self.SingleLocation_SenderName_textbox.toPlainText()
    #         sender_info_singlelocation2 = Shared_B_Credentials_Logic_Page.data[sender_info_singlelocation]
    #         sender_info_singlelocation3 = f'{sender_info_singlelocation} - {sender_info_singlelocation2}'
                
    #         # except Exception as error:
    #         #     error_message = f'You entered an incorrect U#. Please try again.'  # The desired error message
    #         #     QMessageBox.critical(None, "Error", error_message, QMessageBox.StandardButton.Ok)
    #         #     msg.close()
    #         #     return
                    

    #         #RETRIEVE the attached link, implement BeautifulSoup to retrieve the exact link
    #         link_singlelocation2 = self.SingleLocation_AttachLink_textBrowser.toHtml()
    #         soup = BeautifulSoup(link_singlelocation2, 'lxml')
    #         soup2 = soup.find_all('a')
    #         if soup2:
    #             link_singlelocation2 = soup2[0].get('href')
    #         else:
    #             link_singlelocation2 = "No link attached"

                
    #         #RETRIEVE Validity From and To 
    #         ValidityFrom_singlelocation = str(self.SingleLocation_ValidityFrom_textbox.toPlainText())
    #         if ValidityFrom_singlelocation == "":
    #             ValidityFrom_singlelocation = "No 'From' Validity"
                
    #         ValidityTo_singlelocation = str(self.SingleLocation_ValidityTo_textbox.toPlainText())
    #         if ValidityTo_singlelocation == "":
    #             ValidityTo_singlelocation = "No 'To' Validity"
            
        
    #         #RETRIEVE Airline Info
    #         airlineselection = self.SingleLocation_Airline_comboBox.currentText()
    #         if airlineselection == "Select an Airline":
    #             QMessageBox.critical(None, "Error", "Please select a valid airline.", QMessageBox.StandardButton.Ok)
    #             msg.close()
    #             return
            
    #         cscselection = self.SingleLocation_Airline_CSC_comboBox.currentText()
    #         if cscselection == "Select a CSC":
    #             QMessageBox.critical(None, "Error", "Please select a valid csc.", QMessageBox.StandardButton.Ok)
    #             msg.close()
    #             return
            

    #         #RETRIEVE message
    #         projectmessage = self.AdhocTracker_CreateProject_Display.toPlainText()
            
            
    #         #RETRIEVE Priority
    #         priorityselection = self.SingleLocation_Priority_comboBox.currentText()

            
    #         ##########################################################################################################################################
    #         #CREATE THE NAME AND THE FOLDER WHERE ALL THE ATTACHED FILES WILL BE UPLOADED TO
            
    #         current_project_folder_name = f'{airlineselection}-{cscselection} -- {designated_id}'   
            
    #         AdhocTrackerButtonFunctionality.create_projects_folder(current_project_folder_name) 
              
            

    #         ##########################################################################################################################################
    #         #CREATE THE FIRST CONNECTION TO THE DATABASE TO PLACE ALL THE INPUTS INTO THE DATABASE (csc_table_data and currentprojects_data)
            
    #         csc_table_data = {
    #             "project_name" :    [current_project_folder_name], 
    #             "project_id" :      [designated_id], 
    #             "sender" :          [sender_info_singlelocation3],
    #             "hyperlink" :       [link_singlelocation2],
    #             "validity_from" :   [ValidityFrom_singlelocation],
    #             "validity_to" :     [ValidityTo_singlelocation],
    #             "airline" :         [airlineselection], 
    #             "csc1" :            [cscselection], 
    #             "csc2" :            [None], 
    #             "csc3" :            [None], 
    #             "csc4" :            [None], 
    #             "csc5" :            [None], 
    #             "csc6" :            [None],  
    #             "csc7" :            [None],
    #             "csc8" :            [None],
    #             "csc9" :            [None], 
    #             "csc10" :           [None],
    #             "message" :         [projectmessage],
    #             "priority" :        [priorityselection]
    #         }
    #         csc_table_data_df = pd.DataFrame(csc_table_data)
            

    #         currentprojects_data = {
    #             "project_id" :              [designated_id],
    #             "project_name" :            [current_project_folder_name],
    #             'current_department' :      ['Data Management'],
    #             'current_analyst' :         ['Unassigned'],
    #             'status' :                  [''],
    #             'data_analyst' :            [''],
    #             'data_project_started':     [''],
    #             'data_project_ended' :      [''],
    #             'costing_to_data_rework_count' :[0],
    #             'costing_analyst' :         [''],
    #             'costing_project_started':  [''],
    #             'costing_project_ended' :   [''],
    #             'pricing_to_costing_rework_count' :[0],
    #             'pricing_analyst' :         [''],
    #             'pricing_project_started':  [''],
    #             'pricing_project_ended' :   [''],
    #             'priority' :                [priorityselection]
    #         }
    #         currentprojects_df = pd.DataFrame(currentprojects_data)        
    
    
    #         #INSERT INTO THE DATABASE-------------------------------------------------------------------------------------------
    #         conn = sqlite3.connect(AdhocTrackerButtonFunctionality.connectAdhocDatabase())
                        
    #         csc_table_data_df.to_sql(AdhocTrackerButtonFunctionality.csc_table_name, conn, if_exists='append', index=False)
    #         currentprojects_df.to_sql(AdhocTrackerButtonFunctionality.currentproject_table_name, conn, if_exists='append', index=False)
            
    #         conn.commit()             
    #         #conn.close()
            
            
            
    #         ##########################################################################################################################################
    #         #CREATE THE SECOND CONNECTION TO THE DATABASE TO RETRIEVE THE TARGET USERS INFO (users)
            
    #         #This is to retrieve the target users info
    #         conn1 = sqlite3.connect(AdhocTrackerButtonFunctionality.connectUserDatabase())
            
    #         users_managers_df = pd.read_sql('SELECT * FROM users', conn1)
    #         users_managers_df = users_managers_df[(users_managers_df['department'] == 'Data') & (users_managers_df['position'] == 'Manager')]
    #         users_managers_df = users_managers_df['user_id'].tolist()
            
    #         #conn1.close()
            
            
    #         ##########################################################################################################################################
    #         #CREATE THE THIRD CONNECTION TO THE DATABASE TO WRITE TO ADHOC MESSAGES (adhoc_messages)

    #         conn2 = sqlite3.connect(AdhocTrackerButtonFunctionality.connectAdhocDatabase())

    #         for users_managers_df2 in users_managers_df:
    #             #Insert a message into adhoc_messages
    #             adhocmessages_data = {
    #                         "project_name" :                            [current_project_folder_name],
    #                         "sender" :                                  [sender_info_singlelocation3],
    #                         'message_sent_timestamp' :                  [current_date],
    #                         'message_text' :                            [f'A new project has been created'],
    #                         'message_status' :                          ['Unread'],
    #                         'receiver' :                                [users_managers_df2],
    #                         'message_read_timestamp' :                  ['']
    #                     }
    #             adhocmessages_df = pd.DataFrame(adhocmessages_data)    
    #             adhocmessages_df.to_sql(AdhocTrackerButtonFunctionality.adhoc_messages_table_name, conn2, if_exists='append', index=False)        
            
    #         conn2.commit()
    #         #conn2.close()
            

    #         ##########################################################################################################################################
    #         #THE WHOLE SECTION BELOW IS FOR CLEANUP
                        
    #         #REMOVE any contents of the targetfolder
    #         for filename in os.listdir(AdhocTrackerButtonFunctionality.targetfolder):
    #             file_path2 = os.path.join(AdhocTrackerButtonFunctionality.targetfolder, filename)
                
    #             try:
    #                 # Check if it's a file or a directory
    #                 if os.path.isfile(file_path2) or os.path.islink(file_path2):
    #                     os.unlink(file_path2)  # Remove the file or link
                
    #             except Exception as error:
    #                 QMessageBox.critical(None, "Error", str(error), QMessageBox.StandardButton.Ok)
    #                 msg.close()
    #                 return  
                
                
    #         #Clear all the input fields within the App
    #         QMessageBox.information(None, "Success", f"Project has been created", QMessageBox.StandardButton.Ok)
    #         self.SingleLocation_AttachLink_textBrowser.clear()
    #         self.SingleLocation_AttachFile_button.setText("Attach a file")
    #         self.AdhocTracker_CreateProject_Display.clear()
    #         self.SingleLocation_AttachFile_button.setStyleSheet("QPushButton\n"
    #                                                             "{\n"
    #                                                             "color : rgb(0, 0, 0);\n"
    #                                                             "border : 1px solid  rgb(100, 100, 100);\n"
    #                                                             "padding-left: 20px;\n"
    #                                                             "padding-right: 20px;\n"
    #                                                             "border-radius: 4px;\n"
    #                                                             "background-color: rgb(255,255,255);\n"
    #                                                             "\n"
    #                                                             "}\n"
    #                                                             "\n"
    #                                                             "QPushButton:hover {\n"
    #                                                             "\n"
    #                                                             "    padding-left: 20px;\n"
    #                                                             "    padding-right: 20px;\n"
    #                                                             "\n"
    #                                                             "\n"
    #                                                             "    border : 2px solid  rgb(0, 0, 0);\n"
    #                                                             "    \n"
    #                                                             "}\n"
    #                                                             "")
    #         self.SingleLocation_ValidityFrom_textbox.clear()
    #         self.SingleLocation_ValidityTo_textbox.clear()
    #         self.SingleLocation_Airline_comboBox.setCurrentIndex(0)
    #         self.SingleLocation_Airline_CSC_comboBox.setCurrentIndex(0)
    #         self.SingleLocation_Priority_comboBox.setCurrentIndex(0)
    #         msg.close()
            
    #     # except Exception as error:
    #     #     QMessageBox.critical(None, "Error", str(error), QMessageBox.StandardButton.Ok)
    #     #     msg.close()
    #     #     return

    
    # def MultiLocation_Submit_button_Clicked(self,msg): #THIS FUNCTION IS FOR THE MULTIPLELOCATION SUBMISSION  
    #     try:

    #         ######################################################################################################################### 
    #         #RETRIEVE ALL INPUTS
    #         #retrieve the current date
    #         current_date = str(datetime.datetime.now())
            
    #         #Generate an ID      
    #         designated_id = current_date[:16].replace("-", ".").replace(" ", "--").replace(":", ".")
            
            
    #         #RETRIEVE THE USER INFO AND CHECK IF THE INFO MATCHES THE STORED CREDENTIALS
    #         try:
    #             sender_info_multilocation = self.MultiLocation_SenderName_textbox.toPlainText()
    #             sender_info_multilocation2 = Shared_B_Credentials_Logic_Page.data[sender_info_multilocation]
    #             sender_info_multilocation3 = f'{sender_info_multilocation} - {sender_info_multilocation2}'
                
    #         except Exception as error:
    #             error_message = f'You entered an incorrect U#. Please try again.'  # The desired error message
    #             QMessageBox.critical(None, "Error", error_message, QMessageBox.StandardButton.Ok)
    #             msg.close()
    #             return

    #         #RETRIEVE the attached link, implement BeautifulSoup to retrieve the exact link
    #         link_multilocation2 = self.MultipleLocation_AttachLink_textBrowser.toHtml()
    #         soup = BeautifulSoup(link_multilocation2, 'lxml')
    #         soup2 = soup.find_all('a')
    #         if soup2:
    #             link_multilocation = soup2[0].get('href')
                    
    #         else:
    #             link_multilocation = "No link attached"


                
    #         #RETRIEVE Validity From and To 
    #         ValidityFrom_Multilocation = str(self.MultiLocation_ValidityFrom_textbox.toPlainText())
    #         if ValidityFrom_Multilocation == "":
    #             ValidityFrom_Multilocation = "No 'From' Validity"
                
    #         ValidityTo_Multilocation = str(self.MultiLocation_ValidityTo_textbox.toPlainText())
    #         if ValidityTo_Multilocation == "":
    #             ValidityTo_Multilocation = "No 'To' Validity"
            
            
    #         #RETRIEVE Airline Info
    #         airlineselection = self.MultiLocation_Airline_comboBox.currentText()
    #         if airlineselection == "Select an Airline":
    #             QMessageBox.critical(None, "Error", "Please select a valid airline.")
    #             msg.close()
    #             return
            
    #         cscselection1 = self.MultiLocation_CSC_comboBox_1.currentText() 
    #         if cscselection1 == "Select a CSC":
    #             QMessageBox.critical(None, "Error", "Please select a valid csc.")
    #             msg.close()
    #             return
            
    #         cscselection2 = self.MultiLocation_CSC_comboBox_2.currentText()
    #         cscselection3 = self.MultiLocation_CSC_comboBox_3.currentText()
    #         cscselection4 = self.MultiLocation_CSC_comboBox_4.currentText()
    #         cscselection5 = self.MultiLocation_CSC_comboBox_5.currentText()
    #         cscselection6 = self.MultiLocation_CSC_comboBox_6.currentText()
    #         cscselection7 = self.MultiLocation_CSC_comboBox_7.currentText()
    #         cscselection8 = self.MultiLocation_CSC_comboBox_8.currentText()
    #         cscselection9 = self.MultiLocation_CSC_comboBox_9.currentText()
    #         cscselection10 = self.MultiLocation_CSC_comboBox_10.currentText()

    #         #RETRIEVE message
    #         projectmessage = self.AdhocTracker_CreateProject_Display.toPlainText()
            
            
    #         #RETRIEVE Priority
    #         priorityselection = self.MultiLocation_Priority_comboBox.currentText()
            
            
    #         ##########################################################################################################################################
    #         #CREATE THE NAME AND THE FOLDER WHERE ALL THE ATTACHED FILES WILL BE UPLOADED TO
            
    #         current_project_folder_name = f'{airlineselection}-Multi Location -- {designated_id}'
            
    #         AdhocTrackerButtonFunctionality.create_projects_folder(current_project_folder_name)    
            
            
    #         ##########################################################################################################################################
    #         #CREATE THE FIRST CONNECTION TO THE DATABASE TO PLACE ALL THE INPUTS INTO THE DATABASE (csc_table_data and currentprojects_data)
            
    #         csc_table_data = {
    #             "project_name" :    [current_project_folder_name],
    #             "project_id" :      [designated_id], 
    #             "sender" :          [sender_info_multilocation3],
    #             "hyperlink" :       [link_multilocation],
    #             "validity_from" :   [ValidityFrom_Multilocation],
    #             "validity_to" :     [ValidityTo_Multilocation],
    #             "airline" :         [airlineselection], 
    #             "csc1" :            [cscselection1], 
    #             "csc2" :            [cscselection2], 
    #             "csc3" :            [cscselection3], 
    #             "csc4" :            [cscselection4], 
    #             "csc5" :            [cscselection5], 
    #             "csc6" :            [cscselection6], 
    #             "csc7" :            [cscselection7], 
    #             "csc8" :            [cscselection8], 
    #             "csc9" :            [cscselection9], 
    #             "csc10" :           [cscselection10], 
    #             "message" :         [projectmessage],
    #             "priority" :        [priorityselection]
    #         }
    #         csc_table_data_df = pd.DataFrame(csc_table_data)        
        
        
    #         currentprojects_data = {
    #             "project_id" :              [designated_id],
    #             "project_name" :            [current_project_folder_name],
    #             'current_department' :      ['Data Management'],
    #             'current_analyst' :         ['Unassigned'],
    #             'status' :                  [''],
    #             'data_analyst' :            [''],
    #             'data_project_started':     [''],
    #             'data_project_ended' :      [''],
    #             'costing_to_data_rework_count' :[0],
    #             'costing_analyst' :         [''],
    #             'costing_project_started':  [''],
    #             'costing_project_ended' :   [''],
    #             'pricing_to_costing_rework_count' :[0],
    #             'pricing_analyst' :         [''],
    #             'pricing_project_started':  [''],
    #             'pricing_project_ended' :   [''],
    #             'priority' :                [priorityselection]
    #         }
    #         currentprojects_df = pd.DataFrame(currentprojects_data)
                        
            
            
    #         #INSERT INTO THE DATABASE-------------------------------------------------------------------------------------------
    #         conn = sqlite3.connect(AdhocTrackerButtonFunctionality.connectAdhocDatabase())
            
    #         csc_table_data_df.to_sql(AdhocTrackerButtonFunctionality.csc_table_name, conn, if_exists='append', index=False)
    #         currentprojects_df.to_sql(AdhocTrackerButtonFunctionality.currentproject_table_name, conn, if_exists='append', index=False)
            
    #         conn.commit()             
    #         conn.close()   


    #         ##########################################################################################################################################
    #         #CREATE THE SECOND CONNECTION TO THE DATABASE TO RETRIEVE THE TARGET USERS INFO (users)
            
    #         #This is to retrieve the target users info
    #         conn1 = sqlite3.connect(AdhocTrackerButtonFunctionality.connectUserDatabase())
            
    #         users_managers_df = pd.read_sql('SELECT * FROM users', conn1)
    #         users_managers_df = users_managers_df[(users_managers_df['department'] == 'Data') & (users_managers_df['position'] == 'Manager')]
    #         users_managers_df = users_managers_df['user_id'].tolist()
            
    #         conn1.close()

    #         ##########################################################################################################################################
    #         #CREATE THE THIRD CONNECTION TO THE DATABASE TO WRITE TO ADHOC MESSAGES (adhoc_messages)
            
    #         conn2 = sqlite3.connect(AdhocTrackerButtonFunctionality.connectAdhocDatabase())

    #         for users_managers_df2 in users_managers_df:
    #             #Insert a message into adhoc_messages
    #             adhocmessages_data = {
    #                         "project_name" :                            [current_project_folder_name],
    #                         "sender" :                                  [sender_info_multilocation3],
    #                         'message_sent_timestamp' :                  [current_date],
    #                         'message_text' :                            [f'A new project has been created'],
    #                         'message_status' :                          ['Unread'],
    #                         'receiver' :                                [users_managers_df2],
    #                         'message_read_timestamp' :                  ['']
    #                     }
    #             adhocmessages_df = pd.DataFrame(adhocmessages_data)    
    #             adhocmessages_df.to_sql(AdhocTrackerButtonFunctionality.adhoc_messages_table_name, conn2, if_exists='append', index=False)
                
    #         conn2.commit()
    #         conn2.close()
        
        
        

    #         ##########################################################################################################################################
    #         #THE WHOLE SECTION BELOW IS FOR CLEANUP
            
    #         #REMOVE any contents of the targetfolder-------------------------------------------------------------------------
    #         for filename in os.listdir(AdhocTrackerButtonFunctionality.targetfolder):
    #             file_path2 = os.path.join(AdhocTrackerButtonFunctionality.targetfolder, filename)
                
    #             try:
    #                 # Check if it's a file or a directory
    #                 if os.path.isfile(file_path2) or os.path.islink(file_path2):
    #                     os.unlink(file_path2)  # Remove the file or link
                
    #             except Exception as error:
    #                 QMessageBox.critical(None, "Error", str(error), QMessageBox.StandardButton.Ok)
    #                 msg.close()
    #                 return
                
                
                
    #         #Clear all the input fields within the App-------------------------------------------------------------------------
    #         QMessageBox.information(None, "Success", f"Project has been created", QMessageBox.StandardButton.Ok)
    #         self.MultipleLocation_AttachLink_textBrowser.clear()
    #         self.MultiLocation_AttachFile_button.setText("Attach a file")
    #         self.AdhocTracker_CreateProject_Display.clear()
    #         self.MultiLocation_AttachFile_button.setStyleSheet("QPushButton\n"
    #                                                             "{\n"
    #                                                             "color : rgb(0, 0, 0);\n"
    #                                                             "border : 1px solid  rgb(100, 100, 100);\n"
    #                                                             "padding-left: 20px;\n"
    #                                                             "padding-right: 20px;\n"
    #                                                             "border-radius: 4px;\n"
    #                                                             "background-color: rgb(255,255,255);\n"
    #                                                             "\n"
    #                                                             "}\n"
    #                                                             "\n"
    #                                                             "QPushButton:hover {\n"
    #                                                             "\n"
    #                                                             "    padding-left: 20px;\n"
    #                                                             "    padding-right: 20px;\n"
    #                                                             "\n"
    #                                                             "\n"
    #                                                             "    border : 2px solid  rgb(0, 0, 0);\n"
    #                                                             "    \n"
    #                                                             "}\n"
    #                                                             "")
    #         self.MultiLocation_ValidityFrom_textbox.clear()
    #         self.MultiLocation_ValidityTo_textbox.clear()
    #         self.MultiLocation_Airline_comboBox.setCurrentIndex(0)
    #         self.MultiLocation_CSC_comboBox_1.setCurrentIndex(0)
    #         self.MultiLocation_CSC_comboBox_2.setCurrentIndex(0)
    #         self.MultiLocation_CSC_comboBox_3.setCurrentIndex(0)
    #         self.MultiLocation_CSC_comboBox_4.setCurrentIndex(0)
    #         self.MultiLocation_CSC_comboBox_5.setCurrentIndex(0)
    #         self.MultiLocation_CSC_comboBox_6.setCurrentIndex(0)
    #         self.MultiLocation_CSC_comboBox_7.setCurrentIndex(0)
    #         self.MultiLocation_CSC_comboBox_8.setCurrentIndex(0)
    #         self.MultiLocation_CSC_comboBox_9.setCurrentIndex(0)
    #         self.MultiLocation_CSC_comboBox_10.setCurrentIndex(0)
    #         self.MultiLocation_Priority_comboBox.setCurrentIndex(0)
    #         msg.close()
            
            
    #     except Exception as error:
    #         QMessageBox.critical(None, "Error", str(error), QMessageBox.StandardButton.Ok)
    #         msg.close()
    #         return    
  
  
    
    # def Single_AttachFile_button_Clicked(self, msg):    #THIS FUNCTION IS FOR ATTACHING A FILE
    #     try:
            
    #         # Remove any contents of the target folder
    #         for filename in os.listdir(AdhocTrackerButtonFunctionality.targetfolder):
    #             file_path2 = os.path.join(AdhocTrackerButtonFunctionality.targetfolder, filename)
                
    #             try:
    #                 if os.path.isfile(file_path2) or os.path.islink(file_path2):
    #                     os.unlink(file_path2)  # Remove the file or link
    #                 elif os.path.isdir(file_path2):
    #                     # Remove all contents inside the directory, but not the directory itself
    #                     shutil.rmtree(file_path2)  # Remove the directory and all its contents
                
    #             except Exception as error:
    #                 QMessageBox.critical(None, "Error", str(error), QMessageBox.StandardButton.Ok)
    #                 msg.close()
    #                 return  
            

    #         self.SingleLocation_AttachFile_button.setText("Attach a file")
    #         self.SingleLocation_AttachFile_button.setStyleSheet("QPushButton\n"
    #                                                                 "{\n"
    #                                                                 "color : rgb(0,0,0);\n"
    #                                                                 "border : 1px solid  rgb(100, 100, 100);\n"
    #                                                                 "padding-left: 20px;\n"
    #                                                                 "padding-right: 20px;\n"
    #                                                                 "border-radius: 4px;\n"
    #                                                                 "background-color: rgb(255,255,255);\n"
    #                                                                 "\n"
    #                                                                 "}\n"
    #                                                                 "\n"
    #                                                                 "QPushButton:hover {\n"
    #                                                                 "\n"
    #                                                                 "    padding-left: 20px;\n"
    #                                                                 "    padding-right: 20px;\n"
    #                                                                 "\n"
    #                                                                 "\n"
    #                                                                 "    border : 2px solid  rgb(0, 0, 0);\n"
    #                                                                 "    \n"
    #                                                                 "}\n"
    #                                                                 "")
            
            
    #         file_dialog = QFileDialog()
    #         #print(file_dialog)
    #         file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)  # Set file mode to select multiple existing files
    #         file_paths, _ = file_dialog.getOpenFileNames(None, "Select Files", "", "All Files (*.*)")

    #         if not file_paths:
    #             QMessageBox.information(None, "Note", "Attach files cancelled.", QMessageBox.StandardButton.Ok)
    #             msg.close()
    #             return

    #         text_not_allowed = ['(', ')']
    #         for file_path in file_paths:
    #             for text_not_allowed2 in text_not_allowed:
    #                 if text_not_allowed2 in file_path:
    #                     QMessageBox.critical(None, "Error", f"Please rename the file '{file_path}', it contains invalid characters.", QMessageBox.StandardButton.Ok)
    #                     return

    #         # Ensure the target directory exists
    #         os.makedirs(AdhocTrackerButtonFunctionality.targetfolder, exist_ok=True)

    #         for file_path in file_paths:
    #             try:
    #                 # Get the name of the file
    #                 file_name = os.path.basename(file_path)
    #                 #print(file_name)

    #                 # Define the destination path
    #                 destination_path = os.path.join(AdhocTrackerButtonFunctionality.targetfolder, file_name)

    #                 # Copy the file to the target location
    #                 shutil.copy(file_path, destination_path)

    #                 number_of_files = len(file_paths)

    #                 if number_of_files == 1:
    #                     file_name = file_name
                        
    #                 elif number_of_files >= 2:
    #                     file_name = "Multiple Files Attached"
                
    #                 #Change the name of the button to the name of the file / change the color of the text as well
    #                 self.SingleLocation_AttachFile_button.setText(file_name)
    #                 self.SingleLocation_AttachFile_button.setStyleSheet("QPushButton\n"
    #                                                                     "{\n"
    #                                                                     "color : rgb(0, 0, 255);\n"
    #                                                                     "border : 1px solid  rgb(100, 100, 100);\n"
    #                                                                     "padding-left: 20px;\n"
    #                                                                     "padding-right: 20px;\n"
    #                                                                     "border-radius: 4px;\n"
    #                                                                     "background-color: rgb(255,255,255);\n"
    #                                                                     "\n"
    #                                                                     "}\n"
    #                                                                     "\n"
    #                                                                     "QPushButton:hover {\n"
    #                                                                     "\n"
    #                                                                     "    padding-left: 20px;\n"
    #                                                                     "    padding-right: 20px;\n"
    #                                                                     "\n"
    #                                                                     "\n"
    #                                                                     "    border : 2px solid  rgb(0, 0, 0);\n"
    #                                                                     "    \n"
    #                                                                     "}\n"
    #                                                                 "")
    #                 msg.close()
                    
    #             except Exception as error:
    #                 QMessageBox.critical(None, "Error", f"Failed to attach a file", QMessageBox.StandardButton.Ok)
    #                 msg.close()
    #                 return
                
    #     except Exception as error:
    #         QMessageBox.critical(None, "Error", str(error), QMessageBox.StandardButton.Ok)
    #         msg.close()
    #         return   
            
     
    # def Multi_AttachFile_button_Clicked(self, msg):    #THIS FUNCTION IS FOR ATTACHING A FILE
    #     try:
    #         # Remove any contents of the target folder
    #         for filename in os.listdir(AdhocTrackerButtonFunctionality.targetfolder):
    #             file_path2 = os.path.join(AdhocTrackerButtonFunctionality.targetfolder, filename)
                
    #             try:
    #                 if os.path.isfile(file_path2) or os.path.islink(file_path2):
    #                     os.unlink(file_path2)  # Remove the file or link
    #                 elif os.path.isdir(file_path2):
    #                     # Remove all contents inside the directory, but not the directory itself
    #                     shutil.rmtree(file_path2)  # Remove the directory and all its contents
                
    #             except Exception as error:
    #                 QMessageBox.critical(None, "Error", str(error), QMessageBox.StandardButton.Ok)
    #                 msg.close()
    #                 return  
            
    #         self.MultiLocation_AttachFile_button.setText("Attach a file")
    #         self.MultiLocation_AttachFile_button.setStyleSheet("QPushButton\n"
    #                                                                 "{\n"
    #                                                                 "color : rgb(0,0,0);\n"
    #                                                                 "border : 1px solid  rgb(100, 100, 100);\n"
    #                                                                 "padding-left: 20px;\n"
    #                                                                 "padding-right: 20px;\n"
    #                                                                 "border-radius: 4px;\n"
    #                                                                 "background-color: rgb(255,255,255);\n"
    #                                                                 "\n"
    #                                                                 "}\n"
    #                                                                 "\n"
    #                                                                 "QPushButton:hover {\n"
    #                                                                 "\n"
    #                                                                 "    padding-left: 20px;\n"
    #                                                                 "    padding-right: 20px;\n"
    #                                                                 "\n"
    #                                                                 "\n"
    #                                                                 "    border : 2px solid  rgb(0, 0, 0);\n"
    #                                                                 "    \n"
    #                                                                 "}\n"
    #                                                                 "")
            
            
            
    #         file_dialog = QFileDialog()
    #         #print(file_dialog)
    #         file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)  # Set file mode to select multiple existing files
    #         file_paths, _ = file_dialog.getOpenFileNames(None, "Select Files", "", "All Files (*.*)")

    #         if not file_paths:
    #             QMessageBox.information(None, "Note", "Attach files cancelled.", QMessageBox.StandardButton.Ok)
    #             msg.close()
    #             return

    #         text_not_allowed = ['(', ')']
    #         for file_path in file_paths:
    #             for text_not_allowed2 in text_not_allowed:
    #                 if text_not_allowed2 in file_path:
    #                     QMessageBox.critical(None, "Error", f"Please rename the file '{file_path}', it contains invalid characters.", QMessageBox.StandardButton.Ok)
    #                     return

            

    #         # Ensure the target directory exists
    #         os.makedirs(AdhocTrackerButtonFunctionality.targetfolder, exist_ok=True)

    #         for file_path in file_paths:
    #             try:
    #                 # Get the name of the file
    #                 file_name = os.path.basename(file_path)

    #                 # Define the destination path
    #                 destination_path = os.path.join(AdhocTrackerButtonFunctionality.targetfolder, file_name)

    #                 # Copy the file to the target location
    #                 shutil.copy(file_path, destination_path)
                    
                    
    #                 number_of_files = len(file_paths)

    #                 if number_of_files == 1:
    #                     file_name = file_name
                        
    #                 elif number_of_files >= 2:
    #                     file_name = "Multiple Files Attached"
                
                
    #                 #Change the name of the button to the name of the file / change the color of the text as well
    #                 self.MultiLocation_AttachFile_button.setText(file_name)
    #                 self.MultiLocation_AttachFile_button.setStyleSheet("QPushButton\n"
    #                                                                     "{\n"
    #                                                                     "color : rgb(0, 0, 255);\n"
    #                                                                     "border : 1px solid  rgb(100, 100, 100);\n"
    #                                                                     "padding-left: 20px;\n"
    #                                                                     "padding-right: 20px;\n"
    #                                                                     "border-radius: 4px;\n"
    #                                                                     "background-color: rgb(255,255,255);\n"
    #                                                                     "\n"
    #                                                                     "}\n"
    #                                                                     "\n"
    #                                                                     "QPushButton:hover {\n"
    #                                                                     "\n"
    #                                                                     "    padding-left: 20px;\n"
    #                                                                     "    padding-right: 20px;\n"
    #                                                                     "\n"
    #                                                                     "\n"
    #                                                                     "    border : 2px solid  rgb(0, 0, 0);\n"
    #                                                                     "    \n"
    #                                                                     "}\n"
    #                                                                 "")
    #                 msg.close()
                
    #             except Exception as error:
    #                 QMessageBox.critical(None, "Error", f"Failed to attach a file", QMessageBox.StandardButton.Ok)
    #                 msg.close()
    #                 return
            
    #     except Exception as error:
    #         QMessageBox.critical(None, "Error", str(error), QMessageBox.StandardButton.Ok)
    #         msg.close()
    #         return   

