import unittest
import requests
import json
import os
import datetime
# module
from src.scrape import Scrape
from src.date import Date


class Scrape_setup:

    all_data_in_db_dummy = [
        (datetime.date(2022, 4, 2), '196456', '21553495', 77.7951, '1531.5', '129987', '292', '1273538', '132300'),
        (datetime.date(2022, 4, 3), '74053', '21627548', 37.6944, '1457.9', '130029', '42', '1212354', '86400'), 
        (datetime.date(2022, 4, 4), '41129', '21668677', 55.54, '1424.6', '130052', '23', '1184629', '184000'), 
        (datetime.date(2022, 4, 5), '180397', '21849074', 438.613, '1394', '130368', '316', '1159210', '251000'),
        (datetime.date(2022, 4, 6), '214985', '22064059', 119.173, '1322.2', '130708', '340', '1099457', '268000'),
        (datetime.date(2022, 4, 7), '201729', '22265788', 93.834, '1251.3', '131036', '328', '1040481', '255300'), 
        (datetime.date(2022, 4, 8), '175263', '22441051', 86.8804, '1181.2', '131370', '334', '982220', '237300'), 
        (datetime.date(2022, 4, 9), '150675', '22591726', 85.9708, '1141.8', '131679', '309', '949500', '155700')
    ]

    def setup_set_corona_numbers(self, scrape_instance):
        resultjson_de = scrape_instance.request_rki()
        resultjson_de = resultjson_de['features'][0]['attributes']
        return resultjson_de

    def setup_render_chart(self, path):
        os.mkdir(path)

class Scrape_teardown:

    def tear_down_render_chart(self,path, file_list):
        for file in file_list:
            os.remove(path+file)
        os.rmdir(path)


class TestScrape(unittest.TestCase):

    def test_request_rki(self):
        URL = 'https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/rki_key_data_v/FeatureServer/0/query?'
        page = requests.get(url=URL, params={
            'user-agent': 'python-requests/2.9.1',
            'where': f'AdmUnitId = 0',
            'outFields': '*',
            'returnGeometry': False,
            'f': 'json',
            'cacheHint': True}
        )
        expectedOutput = json.loads(page.text)
        self.assertEqual(Scrape().request_rki(), expectedOutput)

    def test_set_corona_numbers(self):
        scrape_instance = Scrape()
        resultjson_de = Scrape_setup().setup_set_corona_numbers(scrape_instance)
        expectedOutput = {
            "new_infection": resultjson_de["AnzFallNeu"],
            "incidenze": resultjson_de["Inz7T"],
            "total_death": resultjson_de["AnzTodesfall"],
            "new_death": resultjson_de["AnzTodesfallNeu"],
            "total_infection": resultjson_de["AnzFall"],
            "SumLast7D": resultjson_de["AnzFall7T"],
            "recoveries": resultjson_de["AnzGenesenNeu"],
        }
        scrape_instance.set_corona_numbers(resultjson_de)

        self.assertDictEqual(scrape_instance.corona_numbers, expectedOutput)

    def test_calculate_difference(self):
        new_value = 10
        basic_value = 50
        difference = new_value * 100 / basic_value
        self.assertEqual(difference, Scrape().calculate_difference(new_value, basic_value))

    def test_render_chart(self):
        path = "./__tests__/render_chart_test/"
        expectedOutput = ["InfectionPerDayChart.png", "TotalInfectionChart.png",
                          "procent.png", "incidence.png", "TotalDeathChart.png", "DeathPerDayChart.png", "recoveries.png"]
        setup = Scrape_setup()
        setup.setup_render_chart(path)
        scrape = Scrape()

        scrape.render_chart(setup.all_data_in_db_dummy, 1, path + 'InfectionPerDayChart', 'Infektionen Pro Tag')
        scrape.render_chart(setup.all_data_in_db_dummy, 2, path + 'TotalInfectionChart', 'Corona Infektionen in Millionen')
        scrape.render_chart(setup.all_data_in_db_dummy, 3, path + 'procent', 'Corona Infektionen in Millionen')
        scrape.render_chart(setup.all_data_in_db_dummy, 4, path + 'incidence', 'incidence')
        scrape.render_chart(setup.all_data_in_db_dummy, 5, path + 'TotalDeathChart', 'Tode durch das Corona Virus')
        scrape.render_chart(setup.all_data_in_db_dummy, 6, path + 'DeathPerDayChart', 'Tode durch das Corona Virus Pro Tag')
        scrape.render_chart(setup.all_data_in_db_dummy, 8, path + 'recoveries', 'recoveries')
        self.assertTrue(os.listdir(path), expectedOutput)

        Scrape_teardown().tear_down_render_chart(path, expectedOutput)

    def test_sort_data_to_x_and_y(self):
        setup = Scrape_setup()

        for i in range(7):
            expected_infection_history = [[],[]]
            for j in range(len(setup.all_data_in_db_dummy)):
                expected_infection_history[0].append(str(setup.all_data_in_db_dummy[j][0]))
                expected_infection_history[1].append(float(setup.all_data_in_db_dummy[j][i+1]))
            expected_date = Date().get_date_in_10_days()
            expectedOutput = [expected_infection_history,expected_date]
            total_infection_history, Previous_Date= Scrape().sort_data_to_x_and_y(setup.all_data_in_db_dummy,i+1)
            Output = [total_infection_history, Previous_Date]
            self.assertEqual(Output,expectedOutput)

if __name__ == '__main__':
    unittest.main()
