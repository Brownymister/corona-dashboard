from dotenv import load_dotenv
import mysql.connector
import os
import plotly.express as px
import requests
import json
import plotly.graph_objs as go
from plotly.offline import iplot
import csv
import time


def split(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


load_dotenv()

mydb = mysql.connector.connect(
    host=os.environ.get('DBHOST'),
    user=os.environ.get('DBUSER'),
    password=os.environ.get('PASSWORD'),
    database=os.environ.get('DB')
)
mycursor = mydb.cursor()
sql = "SELECT * FROM corona;"
mycursor.execute(sql)
myresult = mycursor.fetchall()
infections = []
for i in myresult:
    infections.append(i[1])


def evaluateAverage(infections):
    infections = list(split(infections, 7))
    # 1 - Mittwoch
    # 2 - Donnerstag
    # 3 - Freitag
    # 4 - Sommstag
    # 5 - Sonntag
    # 6 - Monatg
    # 7 - Dienstag
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

    def getAv(weekday):
        weekdaySum = 0
        for i in week[weekday]:
            weekdaySum += int(i)
        weekdayAv = weekdaySum / len(week[weekday])
        return weekdayAv

    classes = ['Mondays', 'Tuesdays', "Wednesdays",
               "Thursdays", "Fridays", "Saturdays", "Sundays"]
    avareges = []

    for class_ in range(len(classes)):
        av = round(getAv(classes[class_]), 5)
        avareges.append(av)
        print(av)
    today = str(time.strftime("%Y-%m-%d"))
    fig = go.Figure(data=go.Bar(y=avareges,
                                x=classes,
                                marker_color='indianred', text=avareges))
    fig.update_layout({"title": "average of day infections",
                       "xaxis": {"title": "Tage"},
                       "yaxis": {"title": "durchschnittliche infektionen"},
                       "showlegend": False})
    fig.write_image(f"./average/av{today}.png", format="png", width=1000, height=600, scale=3)


evaluateAverage(infections)


def getAltersgruppen():
    URL = 'https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_COVID19/FeatureServer/0/query?where=1%3D1&outFields=IdBundesland,Bundesland,Geschlecht,AnzahlFall,NeuerFall,Landkreis,NeuGenesen,Altersgruppe,Datenstand&outSR=4326&f=json'
    result = requests.get(url=URL)  # Anfrage absetzen
    # Das Ergebnis JSON als Python Dictionary laden
    resultjson = json.loads(result.text)

    cases = {
        "age": {
            "A00-A04": {
                "M": 0,
                "W": 0,
            },
            "A05-A14": {
                "M": 0,
                "W": 0,
            },
            "A15-A34": {
                "M": 0,
                "W": 0,
            },
            "A35-A59": {
                "M": 0,
                "W": 0,
            },
            "A60-A79": {
                "M": 0,
                "W": 0,
            },
            "A80+": {
                "M": 0,
                "W": 0,
            },
        }
    }

    classes = ["A00-A04", "A05-A14", "A15-A34", "A35-A59", "A60-A79", "A80+"]

    for i in resultjson['features']:
        for a in classes:
            if i['attributes']['Altersgruppe'] == a:
                if i['attributes']['Geschlecht'] == "M":
                    cases['age'][a]['M'] += (int(i['attributes']
                                             ['AnzahlFall']))
                if i['attributes']['Geschlecht'] == "W":
                    cases['age'][a]['W'] += (int(i['attributes']
                                             ['AnzahlFall']))
        """ if i['attributes']['Altersgruppe'] == "A05-A14":
            if i['attributes']['Geschlecht'] == "M":
                cases['A05-A14']['M'] += (int(i['attributes']['AnzahlFall']))
            if i['attributes']['Geschlecht'] == "W":
                cases['A05-A14']['W'] += (int(i['attributes']['AnzahlFall'])) """
        if i['attributes']['Altersgruppe'] == "unbekannt" or i['attributes']['Geschlecht'] == "unbekannt":
            print(i['attributes']['AnzahlFall'])

    # c mal anz einwohner in altergruppe / gesamt einwohner

    einwohnerM = {
        "A00-A04": 2036084,
        "A05-A14": 3860281,
        "A15-A34": 9815452,
        "A35-A59": 14425614,
        "A60-A79": 8605893,
        "A80+": 2283195,
    }

    resEinwohnerM = 2036084 + 3860281 + 9815452 + 14425614 + 8605893 + 2283195

    lines = []
    with open('/Users/juliank/dev/python/corona/corona/12411-0006.csv', 'r') as readFile:
        reader = csv.reader(readFile)
        for row in reader:
            row[0] = row[0].split(";")
            lines.append(row[0])

    einwohnerW = {
        "A00-A04": 0,
        "A05-A14": 0,
        "A15-A34": 0,
        "A35-A59": 0,
        "A60-A79": 0,
        "A80+": 0,
    }

    for i in range(5):
        einwohnerW['A00-A04'] += int(lines[i][2])

    for i in range(10):
        einwohnerW['A05-A14'] += int(lines[i+5][2])

    for i in range(20):
        einwohnerW['A15-A34'] += int(lines[i+15][2])

    for i in range(25):
        einwohnerW['A35-A59'] += int(lines[i+35][2])

    for i in range(20):
        einwohnerW['A60-A79'] += int(lines[i+60][2])

    for i in range(6):
        einwohnerW['A80+'] += int(lines[i+80][2])

    resEinwohnerW = 0

    for i in einwohnerW:
        resEinwohnerW += einwohnerW[i]

    for i in cases["age"]:
        cases["age"][i]["M"] = (
            (cases["age"][i]["M"] * einwohnerM[i]) / resEinwohnerM)
        cases["age"][i]["W"] = (
            (cases["age"][i]["W"] * einwohnerW[i]) / resEinwohnerW)

    print(cases["age"])
    cm = []
    cw = []
    for i in cases["age"]:
        cm.append(cases["age"][i]["M"])
        cw.append(cases["age"][i]["W"])

    trace1 = go.Bar(
        x=classes,
        y=cm,
        name='Männlich'
    )

    trace2 = go.Bar(
        x=classes,
        y=cw,
        name='Weiblich'
    )

    data = [trace1, trace2, ]
    layout = go.Layout(barmode='stack')
    fig = go.Figure(data=data, layout=layout)
    fig.write_image("byGenderAndAge.png", format="png",
                    width=1000, height=600, scale=3)


getAltersgruppen()


def readCSV():
    lines = []
    with open('/Users/juliank/dev/python/corona/corona/12411-0006.csv', 'r') as readFile:
        reader = csv.reader(readFile)
        for row in reader:
            row[0] = row[0].split(";")
            lines.append(row[0])

    einwohnerW = {
        "A00-A04": 0,
        "A05-A14": 0,
        "A15-A34": 0,
        "A35-A59": 0,
        "A60-A79": 0,
        "A80+": 0,
    }

    for i in range(5):
        einwohnerW['A00-A04'] += int(lines[i][2])

    for i in range(10):
        einwohnerW['A05-A14'] += int(lines[i+5][2])

    for i in range(20):
        einwohnerW['A15-A34'] += int(lines[i+15][2])

    for i in range(25):
        einwohnerW['A35-A59'] += int(lines[i+35][2])

    for i in range(20):
        einwohnerW['A60-A79'] += int(lines[i+60][2])

    for i in range(6):
        einwohnerW['A80+'] += int(lines[i+80][2])
    print(einwohnerW)

    resEinwohnerW = 0

    for i in einwohnerW:
        resEinwohnerW += einwohnerW[i]
