import unittest
import os
# module
from src.render_daily_report import Daily_report
from .scrape_test import Scrape_teardown
from src.date import Date

class TestDaily_report(unittest.TestCase):
    
    def test_render_daily_report_image(self):

        render_daily_repot = Daily_report(1200,1000)

        path = "./__tests__/render_daily_report_test/"

        today = Date().get_formatted_date()
        
        expectedOutput = ["daily_report_"+today+".png"]
        os.mkdir(path)
        
        render_daily_repot.render_daily_report_image(100,10,1000,100,128.123,50,'/__tests__/render_daily_report_test')

        self.assertTrue(set(os.listdir(path)) == set(expectedOutput))

        Scrape_teardown().tear_down_render_chart(path, expectedOutput)
