"""
.. module:: date

.. moduleauthor:: Julian `Brownymister` <Brownymister@gmail.com>

"""

import datetime

class Date:
    
    def get_todays_date(self):
        """
        returns the todays date as datetime object in format YYYY-mm-dd

        :return: format YYYY-mm-dd
        :rtype: datetime object

        """
        today = datetime.date.today()
        return today

    def get_yesterdays_date(self):
        """
        returns the date of the day before as an datetime object

        :return: format YYYY-mm-dd
        :rtype: datetime object
        """
        today = self.get_todays_date()
        yesterday = today - datetime.timedelta(days=1)
        return yesterday

    def get_formatted_date(self):
        """
        returns the formatet date as string

        :return: format YYYY-mm-dd
        :rtype: str
        """
        now = self.get_todays_date()
        today = now.strftime("%Y-%m-%d")
        return today

    def get_date_in_10_days(self):
        """
        returns the date in 10 days as datetime object

        :return: format YYYY-mm-dd
        :rtype: datetime object
        """
        Previous_Date = datetime.datetime.today() + datetime.timedelta(days=10)
        Previous_Date = str(Previous_Date).split(" ")[0]
        return Previous_Date