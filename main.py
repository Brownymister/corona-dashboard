from flask import Flask, Response
from flask import request
from flask import send_file
from scrape import scrape
from dotenv import load_dotenv
import mysql.connector
import schedule
import os
import time
from datetime import datetime
from db import Db
app = Flask(__name__)

scrape()

def get_corona_fromdb(request):
    mydb = Db()
    mycursor = mydb.mycursor

    if request.args.get("date") == None:
        today = time.strftime("%Y-%m-%d")
        sql = "SELECT * FROM corona WHERE date = '"+today+"';"
    else:
        date = request.args.get("date")
        sql = "SELECT * FROM corona WHERE date = '"+date+"';"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult

@app.route('/')
def index():
    return open("./client/index.html", "r").read()

@app.route('/quellen')
def source():
    return open("./client/quellen.html", "r").read()

@app.route('/impfen')
def vaccination():
    return open("./client/vaccination.html", "r").read()

@app.route('/getalldata')
def getalldata():

    myresult = get_corona_fromdb(request)
    if myresult == []:
        scrape()
        myresult = get_corona_fromdb(request)

    mydb = Db()
    mycursor = mydb.mycursor

    get_history = "SELECT * FROM corona;"
    mycursor.execute(get_history)
    history = mycursor.fetchall()
    response = {
        "date":myresult[0][0].strftime("%d.%m.%Y"),
        "new_infection":myresult[0][1],
        "total_infection":myresult[0][2],
        "new_cases_to_total_in_pro":myresult[0][3],
        "incedence_de":myresult[0][4],
        "total_deaths":myresult[0][5],
        "new_deaths":myresult[0][6],
        "days": len(history)
    }
    return response
@app.route("/renderTotalInfectionChart")
def TotalInfectionChart():
    return send_file('./static/TotalInfectionChart.png', mimetype='image/gif')

@app.route("/renderTotalDeathChart")
def TotalDeathChart():
    return send_file('./static/TotalDeathChart.png', mimetype='image/gif')

@app.route("/renderDeathPerDayChart")
def DeathPerDayChart():
    return send_file('./static/DeathPerDayChart.png', mimetype='image/gif')

@app.route("/renderInfectionPerDayChart")
def InfectionPerDayChart():
    return send_file('./static/InfectionPerDayChart.png', mimetype='image/gif')

@app.route("/renderIncidence")
def Incidence():
    return send_file('./static/incidence.png', mimetype='image/gif')

@app.route("/renderAverage")
def renderAverage():
    return send_file('./static/average.png', mimetype='image/gif')

@app.route("/renderDailyReport")
def renderDailyReport():
    now = datetime.now()
    today = now.strftime("%d_%m_%Y")
    return send_file('./daily_reports/daily_report_'+str(today)+'.png', mimetype='image/gif')

app.run(host="0.0.0.0", port="8080")
schedule.every().day.at('07:00').do(scrape)

while 1:
    schedule.run_pending()
    time.sleep(1)