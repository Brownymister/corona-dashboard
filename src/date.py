import datetime

class Date:
    
    def get_todays_date(self):
        today = datetime.date.today()
        return today

    def get_yesterdays_date(self):
        today = self.get_todays_date()
        yesterday = today - datetime.timedelta(days=1)
        return yesterday

    def get_formatted_date(self):
        now = self.get_todays_date()
        today = now.strftime("%Y-%m-%d")
        return today