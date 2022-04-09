import requests
import json
import plotly.graph_objs as go
import datetime
# modules
from .render_daily_report import Daily_report
from .evaluation import Evaluation
from .db import Db
from .date import Date


class Scrape:

    corona_numbers = {
        "new_infection": None,
        "incidenze": None,
        "total_death": None,
        "new_death": None,
        "total_infection": None,
        "SumLast7D": None,
        "recoveries": None,
    }

    def scrape(self):
        mydb = Db()
        mycursor = mydb.mycursor

        self.create_table_if_not_excist(mycursor)

        resultjson_de = self.request_rki()
        resultjson_de = resultjson_de['features'][0]['attributes']

        self.set_corona_numbers(resultjson_de)

        deference_in_pro, db_data_of_yesterday = self.get_diference_of_today_and_yesterday(self.corona_numbers["new_infection"], mydb)

        today = Date().get_todays_date()
        select_data_of_today = "SELECT * FROM corona WHERE date = '"+str(today)+"';"
        db_data_of_today = mydb.execute_sql(select_data_of_today)
        insert_todays_data = f'INSERT INTO corona (date, new_infection,total_infection_de,t_difference_in_pro,incedence,dead, new_death, SumLast7D,recoveries) VALUES ("{today}", {self.corona_numbers["new_infection"]},{self.corona_numbers["total_infection"]}, {str(deference_in_pro)}, {self.corona_numbers["incidenze"]}, {self.corona_numbers["total_death"]},{self.corona_numbers["new_death"]}, {self.corona_numbers["SumLast7D"]}, {self.corona_numbers["recoveries"]})'

        data_of_today_is_in_db = 0 in range(-len(db_data_of_today), len(db_data_of_today))

        if not data_of_today_is_in_db:
            mycursor.execute(insert_todays_data)
            mydb.mydb.commit()
        all_data_in_db = mydb.get_all_data_from_db()

        evaluation = Evaluation()

        evaluation.evaluate_average_per_day(mydb.get_all_new_infections_from_db())
        evaluation.save_average_as_plot("./static/average.png")

        self.render_chart(all_data_in_db, 1, './static/InfectionPerDayChart', 'Infektionen Pro Tag')
        self.render_chart(all_data_in_db, 2, './static/TotalInfectionChart', 'Corona Infektionen in Millionen')
        self.render_chart(all_data_in_db, 3, './static/procent', 'Corona Infektionen in Millionen')
        self.render_chart(all_data_in_db, 4, './static/incidence', 'incidence')
        self.render_chart(all_data_in_db, 5, './static/TotalDeathChart', 'Tode durch das Corona Virus')
        self.render_chart(all_data_in_db, 6, './static/DeathPerDayChart', 'Tode durch das Corona Virus Pro Tag')
        self.render_chart(all_data_in_db, 8, './static/recoveries', 'recoveries')

        Daily_report(1200,1000).render_daily_report_image(
            self.corona_numbers["new_infection"], self.corona_numbers["new_death"], self.corona_numbers["total_infection"], self.corona_numbers["total_death"], self.corona_numbers["incidenze"], db_data_of_yesterday)

    def create_table_if_not_excist(self, mycursor):
        mycursor.execute("CREATE TABLE IF NOT EXISTS corona (date DATE PRIMARY KEY, new_infection longtext,total_infection_de longtext,t_difference_in_pro float, incedence longtext, dead longtext,new_death longtext, SumLast7D varchar(200),recoveries varchar(200));")

    def set_corona_numbers(self, resultjson_de):
        self.corona_numbers["new_infection"] = resultjson_de['AnzFallNeu']
        self.corona_numbers["incidenze"] = resultjson_de['Inz7T']
        self.corona_numbers["total_death"] = resultjson_de['AnzTodesfall']
        self.corona_numbers["new_death"] = resultjson_de['AnzTodesfallNeu']
        self.corona_numbers["total_infection"] = resultjson_de['AnzFall']
        self.corona_numbers["SumLast7D"] = resultjson_de['AnzFall7T']
        self.corona_numbers["recoveries"] = resultjson_de['AnzGenesenNeu']

    def request_rki(self):
        parameter = {
            'user-agent': 'python-requests/2.9.1',
            'where': f'AdmUnitId = 0',
            'outFields': '*',
            'returnGeometry': False,
            'f': 'json',
            'cacheHint': True
        }
        URL = 'https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/rki_key_data_v/FeatureServer/0/query?'
        page = requests.get(url=URL, params=parameter)
        return json.loads(page.text)

    def get_diference_of_today_and_yesterday(self, new_infection, mydb):
        yesterday = Date().get_yesterdays_date()
        get_new_infection_of_yesterday = f'SELECT new_infection FROM corona WHERE date = "{yesterday}"'
        db_data_of_yesterday = mydb.execute_sql(get_new_infection_of_yesterday)
        deference_in_pro = self.calculate_difference(
            int(new_infection), int(db_data_of_yesterday[0][0]))
        return deference_in_pro, db_data_of_yesterday

    def calculate_difference(self, new_value, basic_value):
        new_value = new_value * 100
        return new_value/basic_value

    def render_chart(self, all_data_in_db, a, filename, label_y):
        total_infection_history, Previous_Date = self.sort_data_to_x_and_y(
            all_data_in_db, a)

        fig = go.Figure(
            data=go.Scatter(x=total_infection_history[0],
                            y=total_infection_history[1],
                            marker_color='indianred',
                            text="infections"))
        fig.update_layout(
            {"title": filename,
             "xaxis": {"title": "Datum",
                       'range': ['2020-01-22', Previous_Date]},
             "yaxis": {"title": label_y},
             "showlegend": False}
        )
        fig.write_image(filename+".png",
                        format="png", width=1000, height=600, scale=3)

    def sort_data_to_x_and_y(self, all_data_in_db, a):
        total_infection_history = [[], []]
        dates = []
        for i in range(len(all_data_in_db)):
            total_infection_history[0].append(str(all_data_in_db[i][0]))
            total_infection_history[1].append(float(all_data_in_db[i][a]))
            dates.append(i)
        Previous_Date = datetime.datetime.today() + datetime.timedelta(days=10)
        Previous_Date = str(Previous_Date).split(" ")[0]
        return total_infection_history, Previous_Date
