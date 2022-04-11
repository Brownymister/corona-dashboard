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

    def test_get_date_in_10_days(self):
        today = datetime.date.today()
        td = datetime.timedelta(days=10)
        expectedDate = today + td
        expectedDate = str(expectedDate).split(" ")[0]

        self.assertEqual(expectedDate, Date().get_date_in_10_days())



if __name__ == '__main__':
    unittest.main()