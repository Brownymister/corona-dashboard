import unittest
from dotenv import load_dotenv
import mysql.connector
import os
# module
from src.db import Db


class Setup():

    def setup_data_from_db(self):
        load_dotenv()
        mydb = mysql.connector.connect(
            host=os.environ.get('DBHOST'),
            user=os.environ.get('DBUSER'),
            password=os.environ.get('PASSWORD'),
            database=os.environ.get('DB')
        )
        mycursor = mydb.cursor()
        select_from_date = "SELECT * FROM corona WHERE date = '2022-04-01'"
        mycursor.execute(select_from_date)
        expectedOutput = mycursor.fetchall()
        return expectedOutput

    def setup_get_all_from_db(self):
        load_dotenv()
        mydb = mysql.connector.connect(
            host=os.environ.get('DBHOST'),
            user=os.environ.get('DBUSER'),
            password=os.environ.get('PASSWORD'),
            database=os.environ.get('DB')
        )
        mycursor = mydb.cursor()
        select_from_date = "SELECT * FROM corona"
        mycursor.execute(select_from_date)
        expectedOutput = mycursor.fetchall()
        return expectedOutput


class TestDb(unittest.TestCase):

    def test_execute_sql(self):
        load_dotenv()
        mydb = mysql.connector.connect(
            host=os.environ.get('DBHOST'),
            user=os.environ.get('DBUSER'),
            password=os.environ.get('PASSWORD'),
            database=os.environ.get('DB')
        )
        mycursor = mydb.cursor()
        select_from_date = "SELECT * FROM corona WHERE date = '2022-04-01'"
        mycursor.execute(select_from_date)
        expectedOutput = mycursor.fetchall()
        statement = "SELECT * FROM corona WHERE date = '2022-04-01'"
        self.assertEqual(Db().execute_sql(statement), expectedOutput)
        
    def test_get_data_fromdb_by_date(self):
        expectedOutput = Setup().setup_data_from_db()
        self.assertEqual(Db().get_data_fromdb_by_date(
            '2022-04-01'), expectedOutput)

    def test_get_all_data_from_db(self):
        expectedOutput = Setup().setup_get_all_from_db()
        self.assertEqual(Db().get_all_data_from_db(), expectedOutput)
    
    def test_get_all_new_infections_from_db(self):
        load_dotenv()
        mydb = mysql.connector.connect(
            host=os.environ.get('DBHOST'),
            user=os.environ.get('DBUSER'),
            password=os.environ.get('PASSWORD'),
            database=os.environ.get('DB')
        )
        mycursor = mydb.cursor()
        select_all_from_db = "SELECT * FROM corona"
        mycursor.execute(select_all_from_db)
        all_from_db = mycursor.fetchall()
        expectedOutput = []
        for i in all_from_db:
            expectedOutput.append(i[1])

        self.assertEqual(Db().get_all_new_infections_from_db(), expectedOutput)


if __name__ == '__main__':
    unittest.main()
