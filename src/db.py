from dotenv import load_dotenv
import mysql.connector
import os
from .date import Date

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

    def execute_sql(self, statment):
        self.mycursor.execute(statment)
        myresult = self.mycursor.fetchall()
        return myresult

    def get_all_data_from_db(self):
        sql = "SELECT * FROM corona"
        self.mycursor.execute(sql)
        myresult = self.mycursor.fetchall()
        return myresult

    def get_data_fromdb_by_date(self, date):
        request_not_gives_date_param = date == None

        if request_not_gives_date_param:
            today = Date().get_formatted_date()
            select_data_by_date = "SELECT * FROM corona WHERE date = '"+today+"';"
        else:
            select_data_by_date = "SELECT * FROM corona WHERE date = '"+date+"';"
        data_by_date = self.execute_sql(select_data_by_date)
        
        return data_by_date