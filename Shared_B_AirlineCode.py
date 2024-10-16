from PyQt6.QtWidgets import  QFileDialog, QMessageBox

import pandas as pd, sqlite3, os

#Path for the current projects
directory_path = r"M:\LSGN\ARHD38-LSGN1\everyone\Analytica\Z)AnalyticaDataBase\AdhocTracker\AdhocTracker_CurrentProjects\AllProjects"
    
#UserDatabase - Table
airline_code = 'airline_code'

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


#Establish the connection to retrieve the list of the airline and csc
conn1 = sqlite3.connect(connectUserDatabase())

airline_df = pd.read_sql("SELECT * FROM airline_code", conn1)
airline_code = airline_df['airline_name'].to_dict().values()

csc_df = pd.read_sql("SELECT * FROM csc_code", conn1)
csc = csc_df['csc_name'].to_dict().values()

conn1.close()
