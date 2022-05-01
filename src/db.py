"""
.. module:: date

.. moduleauthor:: Julian `Brownymister` <Brownymister@gmail.com>

"""

from dotenv import load_dotenv
import mysql.connector
import os
from .date import Date

class Db:

    mycursor = None
    mydb = None
    def __init__(self):
        """iniciates the database connection
        """
        load_dotenv()
        self.mydb = mysql.connector.connect(
            host=os.environ.get('DBHOST'),
            user=os.environ.get('DBUSER'),
            password=os.environ.get('PASSWORD'),
            database=os.environ.get('DB')
        )
        self.mycursor = self.mydb.cursor()

    def execute_sql(self, statment:str)->list:
        """takes an sql select statement and executes it on the database

        Args:
            statment (str): sql select statement

        Returns:
            list: databse response
        """
        self.mycursor.execute(statment)
        myresult = self.mycursor.fetchall()
        return myresult

    def get_all_data_from_db(self) -> list:
        """returns all entries in the databse

        Returns:
            list: databse response
        """
        sql = "SELECT * FROM corona"
        self.mycursor.execute(sql)
        myresult = self.mycursor.fetchall()
        return myresult

    def get_data_fromdb_by_date(self, date) -> list:
        """gets database entry by date

        Args:
            date (str): date string to select from db

        Returns:
            list: databse response
        """
        request_not_gives_date_param = date == None

        if request_not_gives_date_param:
            today = Date().get_formatted_date()
            select_data_by_date = "SELECT * FROM corona WHERE date = '"+today+"';"
        else:
            select_data_by_date = "SELECT * FROM corona WHERE date = '"+date+"';"
        data_by_date = self.execute_sql(select_data_by_date)
        
        return data_by_date

    def get_all_new_infections_from_db(self) ->list:
        """get from every entry in the databse the collum `new infection`

        Returns:
            list: databse response
        """
        mydb = Db()
        all_data_from_db = mydb.get_all_data_from_db()
        infections = []
        for i in all_data_from_db:
            infections.append(i[1])
        return infections