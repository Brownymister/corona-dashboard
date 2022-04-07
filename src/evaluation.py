import plotly.graph_objs as go
# modules
from .db import Db


class Evaluation:

    def evaluate_average(self, infections):
        infections = list(self.split_array_to_smaler_arrays(infections, 7))

        week = {
            "Mondays": [],
            "Tuesdays": [],
            "Wednesdays": [],
            "Thursdays": [],
            "Fridays": [],
            "Saturdays": [],
            "Sundays": [],
        }

        for i in infections:
            week['Wednesdays'].append(i[0])
            if len(i) >= 2:
                week['Thursdays'].append(i[1])
            if len(i) >= 3:
                week['Fridays'].append(i[2])
            if len(i) >= 4:
                week['Saturdays'].append(i[3])
            if len(i) >= 5:
                week['Sundays'].append(i[4])
            if len(i) >= 6:
                week['Mondays'].append(i[5])
            if len(i) >= 7:
                week['Tuesdays'].append(i[6])

        classes = ['Mondays', 'Tuesdays', "Wednesdays",
                   "Thursdays", "Fridays", "Saturdays", "Sundays"]
        avareges = []

        for class_ in range(len(classes)):
            average = round(self.get_average(classes[class_], week), 5)
            avareges.append(average)
            print(average)
        
        self.save_average_as_plot(classes, avareges)

    def split_array_to_smaler_arrays(self,array, number_of_parts):
        for i in range(0, len(array), number_of_parts):
            yield array[i:i + number_of_parts]


    def get_average(self, weekday, week):
        weekdaySum = 0
        for i in week[weekday]:
            weekdaySum += int(i)
        weekdayAv = weekdaySum / len(week[weekday])
        return weekdayAv

    def save_average_as_plot(self, classes, avareges) -> None:
        fig = go.Figure(data=go.Bar(y=avareges,
                                    x=classes,
                                    marker_color='indianred', text=avareges))
        fig.update_layout({"title": "average of day infections",
                           "xaxis": {"title": "Tage"},
                           "yaxis": {"title": "durchschnittliche infektionen"},
                           "showlegend": False})
        fig.write_image(f"./static/average.png", format="png",
                        width=1000, height=600, scale=3)

    def get_all_new_infections_from_db(self):
        mydb = Db()
        all_data_from_db = mydb.get_all_data_from_db()
        infections = []
        for i in all_data_from_db:
            infections.append(i[1])
        return infections