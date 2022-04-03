import csv
from jinja2 import Undefined
""" import matplotlib.pyplot as plt """
import mysql.connector
from dotenv import load_dotenv
import os
""" from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas """
load_dotenv()

mydb = mysql.connector.connect( 
        host= os.environ.get('DBHOST'), 
        user= os.environ.get('DBUSER'),
        password= os.environ.get('PASSWORD'),
        database= os.environ.get('DB')
)
mycursor = mydb.cursor()
total_death_history = []
total_infection_history = []
def f():
    lines = []
    with open('/Users/juliank/dev/python/corona/corona/corona-recoveries.csv', 'r') as readFile:
        reader = csv.reader(readFile)
        for row in reader:
            lines.append(row)
            for field in row:
                if 'Date' in field:
                    lines.remove(row)

    with open('/Users/juliank/dev/python/corona/corona/corona-recoveries.csv', 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(lines)
    with open('/Users/juliank/dev/python/corona/corona/corona-recoveries.csv', 'r') as csv_datei:
        reader = csv.reader(csv_datei, delimiter='\t')
        # last_in = 0
        for zeile in reader:
            if zeile[0] == 'Date':
                reader.remove(zeile)
                return
            total_infection_history.append(zeile[67])
            recoveries = zeile[67]
            # new_death = int(zeile[67]) - int(last_in)
            today = zeile[0]
            if today == '2021-11-28' or today == '2021-11-28':
                print(' ')
            else:
                # last_in = zeile[67]
                sql = f'UPDATE corona SET recoveries = "{recoveries}" WHERE date = "{today}"'
                # sql = f"""INSERT INTO corona (date, new_infection,total_infection_de)
                #        SELECT * FROM (SELECT '{today}' AS date, '{new_infection}' AS new_infection, '{total_infection}' AS total_infection_de) AS temp
                #        WHERE NOT EXISTS (
                #            SELECT date FROM corona WHERE date = '{today}'
                #        ) LIMIT 1;"""
                print(sql)
                mycursor.execute(sql)
                mydb.mydb.commit()

def updateDifference():
    sql = "SELECT * FROM corona;"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    for i in range(len(myresult)):
        if myresult[i][2] == '0' or myresult[i][1] == '0' or int(myresult[i-1][1]) == 0:
            pass
        else:
            if i == 0:
                deference_in_pro = 0
            else:
                deference_in_pro = calculate_difference(int(myresult[i][1]),int(myresult[i-1][1]))
            sql = f'UPDATE corona SET t_difference_in_pro = {deference_in_pro} WHERE date = "{str(myresult[i][0])}"'
            print(sql)
            mycursor.execute(sql)
            mydb.mydb.commit()

def calculate_difference(w,p):
    w = w *100
    return w/p

def setsum7D():
    sql = "SELECT * FROM corona;"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    for i in range(len(myresult)) :
        if myresult[i][2] == '0' or myresult[i][1] == '0' or int(myresult[i-1][2]) == 0:
            pass
        else:
            if myresult[i][7] == None: # ! ------
                SumLast7D = int(myresult[i][2]) - int(myresult[i-7][2]) 
                print(SumLast7D)
                if SumLast7D > 0:
                    sql = f'UPDATE corona SET SumLast7D = {SumLast7D} WHERE date = "{str(myresult[i][0])}"'
                    print(sql)
                    mycursor.execute(sql)
                    mydb.mydb.commit()

def updateincedenze():
    sql = "SELECT * FROM corona;"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    for i in range(len(myresult)) :
        if myresult[i][2] == '0' or myresult[i][1] == '0' or int(myresult[i-1][2]) == 0:
            pass
        else:
            if myresult[i][4] == None and myresult[i][7] != None:
                a = int(myresult[i][7])
                b = a / 83200000
                incidenz = b * 100000
                incidenz = round(incidenz,1)
                sql = f'UPDATE corona SET incedence = {incidenz} WHERE date = "{str(myresult[i][0])}"'
                print(sql)
                mycursor.execute(sql)
                mydb.mydb.commit()


""" sql = "SELECT * FROM corona;"
mycursor.execute(sql)
myresult = mycursor.fetchall()
myresult = myresult[-49:]

Dates = []
Close = []

for i in myresult:
    Dates.append(str(i[0]))
    Close.append(str(i[2]))

with open('Date.txt', 'w') as f:
    for i in Dates:
        f.write("'"+i + "', ")
with open('Close.txt', 'w') as f:
    for i in Close:
        f.write(i + ", ") """

updateDifference()