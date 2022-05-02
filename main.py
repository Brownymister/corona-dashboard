from flask import Flask, request, send_file
import schedule
import time
import os
import logging
# modules
from src.db import Db
from src.scrape import Scrape
from src.date import Date
from src.render_daily_report import Daily_report

app = Flask(__name__)

Scrape().scrape()

# logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
 
@app.route('/blogs')
def blog():
    app.logger.info('Info level log')
    app.logger.warning('Warning level log')
    return f"Welcome to the Blog"
 
app.run(host='localhost', debug=True)



@app.route('/')
def index():
    return open("./client/index.html", "r").read()

@app.route('/getalldata')
def getalldata():
    mydb = Db()

    myresult = mydb.get_data_fromdb_by_date(request.args.get("date"))
    if myresult == []:
        Scrape().scrape()
        myresult = Db().get_data_fromdb_by_date(request.args.get("date"))

    history = mydb.get_all_data_from_db()

    response = {
        "date": myresult[0][0].strftime("%d.%m.%Y"),
        "new_infection": myresult[0][1],
        "total_infection": myresult[0][2],
        "new_cases_to_total_in_pro": myresult[0][3],
        "incedence_de": myresult[0][4],
        "total_deaths": myresult[0][5],
        "new_deaths": myresult[0][6],
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
    today = Date().get_formatted_date()
    daily_repots = os.listdir("./daily_reports/")
    if 'daily_report_'+str(today)+'.png' not in daily_repots:
        Scrape().scrape()   
     
    return send_file('./daily_reports/daily_report_'+str(today)+'.png', mimetype='image/gif')


app.run(host="0.0.0.0", port="8080")
schedule.every().day.at('07:00').do(Scrape().scrape)

while 1:
    schedule.run_pending()
    time.sleep(1)
