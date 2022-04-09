import unittest
# modules
from src.date import Date
import datetime

class TestDate(unittest.TestCase):

    def test_get_todays_date(self):
        self.assertEqual(datetime.date.today(), Date().get_todays_date())

    def test_get_yesterdays_date(self):
        date = Date()
        yesterday = datetime.date.today() - datetime.timedelta(1)
        self.assertEqual(yesterday,date.get_yesterdays_date())

    def test_get_formatted_date(self):
        date = Date()
        expectedOutput = datetime.date.today().strftime("%Y-%m-%d")
        self.assertEqual(date.get_formatted_date(), expectedOutput)

if __name__ == '__main__':
    unittest.main()