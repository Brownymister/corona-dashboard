import unittest
# module
from src.scrape import Scrape
from src.date import Date
from src.db import Db


class Setup:

    def setup_delete_newest_entry_in_db(self):
        mydb = Db()
        mycursor = mydb.mycursor

        delete_new_entry_from_db = "DELETE FROM corona WHERE date = '"+Date().get_formatted_date()+"';"
        mycursor.execute(delete_new_entry_from_db)
        mydb.mydb.commit()

    def setup_set_expected_output(self):
        mydb = Db()
        self.expectedOutput = mydb.execute_sql("SELECT * FROM corona WHERE date = '"+Date().get_formatted_date()+"';")

class TestScrapeDb(unittest.TestCase):

    def test_screape(self):
        setup = Setup()
        setup.setup_set_expected_output()
        setup.setup_delete_newest_entry_in_db()
        Scrape().scrape()
        output =  Db().execute_sql("SELECT * FROM corona WHERE date = '"+Date().get_formatted_date()+"';")
        self.assertEqual(output, setup.expectedOutput)