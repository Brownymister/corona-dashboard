from dotenv import load_dotenv
import mysql.connector
import os

class Db:

    mycursor = None
    mydb = None
    def __init__(self):
        load_dotenv()
        self.mydb = mysql.connector.connect(
            host=os.environ.get('DBHOST'),
            user=os.environ.get('DBUSER'),
            password=os.environ.get('PASSWORD'),
            database=os.environ.get('DB')
        )
        self.mycursor = self.mydb.cursor()