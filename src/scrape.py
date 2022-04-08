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

    def scrape(self):
        mydb = Db()
        mycursor = mydb.mycursor

        mycursor.execute("CREATE TABLE IF NOT EXISTS corona (date DATE, new_infection longtext,total_infection_de longtext,t_difference_in_pro float, incedence longtext, dead longtext,new_death longtext, PRIMARY KEY (date));")

        resultjson_de = self.request_rki()
        resultjson_de = resultjson_de['features'][0]['attributes']

        new_infection = resultjson_de['AnzFallNeu']
        incidenze = resultjson_de['Inz7T']
        total_death = resultjson_de['AnzTodesfall']
        new_death = resultjson_de['AnzTodesfallNeu']
        total_infection = resultjson_de['AnzFall']
        SumLast7D = resultjson_de['AnzFall7T']
        recoveries = resultjson_de['AnzGenesenNeu']

        deference_in_pro, db_data_of_yesterday = self.get_diference_of_today_and_yesterday(
            new_infection, mydb)

        today = Date().get_todays_date()
        select_data_of_today = "SELECT * FROM corona WHERE date = '"+str(today)+"';"
        db_data_of_today = mydb.execute_sql(select_data_of_today)
        insert_todays_data = f'INSERT INTO corona (date, new_infection,total_infection_de,t_difference_in_pro,incedence,dead, new_death, SumLast7D,recoveries) VALUES ("{today}", {new_infection},{total_infection}, {str(deference_in_pro)}, {incidenze}, {total_death},{new_death}, {SumLast7D}, {recoveries})'

        data_of_today_is_in_db = 0 in range(-len(db_data_of_today), len(db_data_of_today))
        # data_of_today_is_not_data_in_db = str(db_data_of_today[0][0]) != str(today)

        if not data_of_today_is_in_db:
            mycursor.execute(insert_todays_data)
            mydb.mydb.commit()
        all_data_in_db = mydb.get_all_data_from_db()

        Evaluation().evaluate_average(Evaluation().get_all_new_infections_from_db())

        self.render_chart(all_data_in_db, 2, 'TotalInfectionChart',
                          'Corona Infektionen in Millionen')
        self.render_chart(all_data_in_db, 3, 'procent',
                          'Corona Infektionen in Millionen')
        self.render_chart(all_data_in_db, 1,
                          'InfectionPerDayChart', 'Infektionen Pro Tag')
        self.render_chart(all_data_in_db, 5, 'TotalDeathChart',
                          'Tode durch das Corona Virus')
        self.render_chart(all_data_in_db, 6, 'DeathPerDayChart',
                          'Tode durch das Corona Virus Pro Tag')
        self.render_chart(all_data_in_db, 4, 'incidence', 'incidence')
        self.render_chart(all_data_in_db, 8, 'recoveries', 'recoveries')

        Daily_report(1200,1000).render_daily_report_image(
            new_infection, new_death, total_infection, total_death, incidenze, db_data_of_yesterday)

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

    def calculate_difference(self, w, p):
        w = w * 100
        return w/p

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
        fig.write_image("./static/"+filename+".png",
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
