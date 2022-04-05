import requests
import json
import plotly.graph_objs as go
import datetime
import time
# modules
from render_daily_report import render_daily_report_image
from evaluation import evaluateAverage , get_all_new_infections_from_db
from db import Db

def calculate_difference(w,p):
    w = w *100
    return w/p

def scrape():
    mydb = Db()
    mycursor = mydb.mycursor

    mycursor.execute("CREATE TABLE IF NOT EXISTS corona (date DATE, new_infection longtext,total_infection_de longtext,t_difference_in_pro float, incedence longtext, dead longtext,new_death longtext, PRIMARY KEY (date));")
    
    resultjson_de = request_rki()
    resultjson_de = resultjson_de['features'][0]['attributes']

    new_infection = resultjson_de['AnzFallNeu']
    incidenze = resultjson_de['Inz7T']
    total_death = resultjson_de['AnzTodesfall']
    new_death = resultjson_de['AnzTodesfallNeu']
    total_infection = resultjson_de['AnzFall']
    SumLast7D = resultjson_de['AnzFall7T']
    recoveries = resultjson_de['AnzGenesenNeu']

    today = datetime.date.today()

    yesterday = today - datetime.timedelta(days=1)
    get_new_infection_of_yesterday = f'SELECT new_infection FROM corona WHERE date = "{yesterday}"'
    mycursor.execute(get_new_infection_of_yesterday)
    myresult_yesterday = mycursor.fetchall()

    deference_in_pro = calculate_difference(int(new_infection),int(myresult_yesterday[0][0]))
    today = time.strftime("%Y-%m-%d")
    sql = "SELECT * FROM corona WHERE date = '"+today+"';"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    sql = f'INSERT INTO corona (date, new_infection,total_infection_de,t_difference_in_pro,incedence,dead, new_death, SumLast7D,recoveries) VALUES ("{today}", {new_infection},{total_infection}, {str(deference_in_pro)}, {incidenze}, {total_death},{new_death}, {SumLast7D}, {recoveries})'
    if myresult:
        if str(myresult[0][0]) != str(today):
            mycursor.execute(sql)
            mydb.mydb.commit()
    else:
        mycursor.execute(sql)
        mydb.mydb.commit()
    sql = "SELECT * FROM corona"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    evaluateAverage(get_all_new_infections_from_db())

    renderAllCharts(myresult,2,'TotalInfectionChart','Corona Infektionen in Millionen')
    renderAllCharts(myresult,3,'procent','Corona Infektionen in Millionen')
    renderAllCharts(myresult,1,'InfectionPerDayChart','Infektionen Pro Tag')
    renderAllCharts(myresult,5,'TotalDeathChart','Tode durch das Corona Virus')
    renderAllCharts(myresult,6,'DeathPerDayChart','Tode durch das Corona Virus Pro Tag')
    renderAllCharts(myresult,4,'incidence','incidence')
    renderAllCharts(myresult,8,'recoveries','recoveries')

    render_daily_report_image(new_infection, new_death, total_infection, total_death, incidenze, myresult_yesterday)

def renderAllCharts(myresult,a,filename,label_y):
    total_infection_history = [[],[]]
    dates = []
    for i in range(len(myresult)):
        total_infection_history[0].append(str(myresult[i][0]))
        total_infection_history[1].append(float(myresult[i][a]))
        dates.append(i)
    Previous_Date = datetime.datetime.today() + datetime.timedelta(days=10)
    Previous_Date = str(Previous_Date).split(" ")[0]

    fig = go.Figure(data=go.Scatter(x=total_infection_history[0],  
                        y=total_infection_history[1],
                        marker_color='indianred', text="infections"))
    fig.update_layout({"title": filename,
                   "xaxis": {"title":"Datum",
                   'range':['2020-01-22', Previous_Date]},
                   "yaxis": {"title":label_y},
                   "showlegend": False})
    fig.write_image("./static/"+filename+".png",format="png", width=1000, height=600, scale=3)

def request_rki():
    parameter = {
    'user-agent':'python-requests/2.9.1',
    'where': f'AdmUnitId = 0', # Welche landkreise sollen zurück gegeben werden
    'outFields': '*', # Rückgabe aller Felder
    'returnGeometry': False, # Keine Geometrien
    'f':'json', # Rückgabeformat, hier JSON
    'cacheHint': True # Zugriff über CDN anfragen
    } 
    URL = 'https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/rki_key_data_v/FeatureServer/0/query?'
    page = requests.get(url=URL, params=parameter)
    return json.loads(page.text)

# scrape()