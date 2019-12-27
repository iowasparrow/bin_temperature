from flask import Flask, render_template, send_file, make_response, request, url_for
import sqlite3
import os
from werkzeug.utils import redirect
from datetime import datetime, timezone, timedelta
import createTable as createTable
import pprint

app = Flask(__name__)

alert_text_file = '/var/www/html/binweb/bin_temperature/alert_file.txt'
#database = '/home/gsiebrecht/PycharmProjects/bin_temperature/sensorsData.db'
#database = 'sensorsData.db'
database = '/var/www/html/binweb/bin_temperature/sensorsData.db'
site_id = 1

def get_all():  # this is for the chart
    conn = sqlite3.connect(database, check_same_thread=False)
    curs = conn.cursor()
    curs.execute("SELECT * FROM DHT_data ORDER BY timestamp DESC")
    data = curs.fetchall()
    dates = []
    temps = []
    # siteids = []
    soiltemps = []
    sensor1 = []
    # sensor2 = []
    # sensor3 = []
    # sensor4 = []
    # sensor5 = []
    # sensor6 = []
    for row in reversed(data):
        dates.append(row[0])
        temps.append(row[1])
        #siteids.append(row[2])
        soiltemps.append(row[3])
        #sensor1.append(row[4])
        
        if row[4] == 0:
            sensor1.append('null')
        else:
            sensor1.append(row[4])
        
        # sensor2.append(row[5])
        # sensor3append(row[6])
        # sensor4.append(row[7])
        # sensor5.append(row[8])
        # sensor6.append(row[9])

    conn.close()
    return dates, temps, soiltemps, sensor1

@app.route("/reset", methods=['GET', 'POST'])
def something():
    createTable.reset()
    return("table was reset")


# @app.route("/reset", methods=['GET', 'POST'])
# def createTable():
#     reset_table.drop_table()
#     print("table reset")
#     return "table reset"


def number_records():  # display number of recoreds
    conn = sqlite3.connect(database, check_same_thread=False)
    curs = conn.cursor()
    curs.execute("SELECT COUNT (*) FROM DHT_data")
    datapoints = curs.fetchall()
    # print('\nTotal rows: {}'.format(datapoints[0][0]))
    # print("here")
    conn.close()
    return datapoints[0][0]


def check_rapid_rise(current_temp):
    conn = sqlite3.connect(database, check_same_thread=False)
    curs = conn.cursor()
    temp_week_ago = 0
    for row in curs.execute(
            "SELECT * FROM DHT_data WHERE timestamp BETWEEN datetime('now', '-8 days') AND datetime('now', '-6 days') LIMIT 1;"):
        temp_week_ago = row[1]
    conn.close()
    temp_difference = current_temp - temp_week_ago
    print('temp difference=', temp_difference)
    if temp_difference >= 3 and current_temp > 32:
        print("DANGER RAPID RISE DETECTED 3 degrees in one week at 32.")
        set_temp_alarm('true')
        temp_difference_rounded = round(temp_difference, 2)
        return temp_difference_rounded, temp_week_ago
    else:
        temp_difference_rounded = round(temp_difference, 2)
        return temp_difference_rounded, temp_week_ago

def create_timer():
    conn = sqlite3.connect(database)
    curs = conn.cursor()
    timestamp = datetime.now()
    curs.execute("INSERT INTO tbl_timer values((?))", (timestamp,))
    conn.commit()
    conn.close()

def check_timer():
    conn = sqlite3.connect(database)
    curs = conn.cursor()
    timer_start = []
    for row in curs.execute("SELECT * FROM tbl_timer"):
        timer_start = row[0]
    conn.close()
    #print(timer_start)
    now = datetime.now()
    timer_started = datetime.strptime(timer_start, '%Y-%m-%d %H:%M:%S.%f')
    delta = now - timer_started
    fixed_delta = timedelta(seconds=8000)  #8000=2 hours
    if delta > fixed_delta:
        print("timer function says cancel, timer enough time has passed")
        cancel = True
    else:
        print("check timer function in timer modules returns false ")
        cancel = False

    #print(delta)
    print('delta seconds=', delta.seconds)
    print('delta days=', delta.days)
    return cancel

def set_temp_alarm(temp_alarm):  # we expect a string of true check status
    # alert_file = open("alert_file.txt", "w") # create the alert file
    if temp_alarm == 'true':
        if check_timer() == True:
            if os.path.exists(alert_text_file):
                alert_file = open(alert_text_file, "rt")
                if alert_file.readline() == 'true':
                    alert_file.close()
                    print("file contents=True close it and return true")
                    return 'true'
                else:
                    alert_file = open(alert_text_file, "w")
                    alert_file.write("true")
                    alert_file.close()
                    print("file contents were overwritten")
                return 'true'
            else:
                alert_file = open(alert_text_file, "w")
                alert_file.write("true")
                alert_file.close()
                os.chmod(alert_text_file, 0o777)
                print("File Created")

    if temp_alarm == 'check_status':
        if os.path.exists(alert_text_file):
            alert_file = open(alert_text_file, "rt")  # open the file for reading
            temp_alarm = alert_file.readline()
            alert_file.close()
            # print("checking status of temp alarm")
            return temp_alarm


def get_current_data():  # get current values for display on web page
    conn = sqlite3.connect(database, check_same_thread=False)
    curs = conn.cursor()
    current_time = []
    current_temp = []
    current_soiltemp = []
    for row in curs.execute("SELECT * FROM DHT_data ORDER BY timestamp DESC LIMIT 1"):
        current_time = str(row[0])
        current_temp = row[1]
        current_soiltemp = row[3]
    conn.close()
    temp_difference, temp_week_ago = check_rapid_rise(current_temp)
    return current_time, current_temp, temp_difference, temp_week_ago, current_soiltemp


@app.route("/grid", methods=['GET', 'POST'])
def grid():
    current_time, current_temp, temp_difference, temp_week_ago, current_soiltemp,sensor1 = get_current_data()
    dates, temps, soiltemps = get_all()
    rows = number_records()
    temp_alarm = set_temp_alarm("check_status")
    #pin_status = check_relay_status()
    pin_status = False

    return render_template('grid.html', temp_week_ago=temp_week_ago, current_soiltemp=current_soiltemp, sensor1=sensor1, temp_difference=temp_difference,
                           temp_alarm=temp_alarm, temps=temps, soiltemps=soiltemps, dates=dates, current_time=current_time,
                           rows=rows, current_temp=current_temp, pin_status=pin_status, server_up="yes")


@app.route("/", methods=['GET', 'POST'])
def index():
    current_time, current_temp, temp_difference, temp_week_ago, current_soiltemp = get_current_data()
    dates, temps, soiltemps, sensor1 = get_all()
    rows = number_records()
    temp_alarm = set_temp_alarm("check_status")
    #pin_status = check_relay_status()
    pin_status = False

    if "clear_alarm" in request.form:
        print("button pressed")
        alert_file = open(alert_text_file, "w")
        alert_file.write("false")
        alert_file.close()
        os.chmod(alert_text_file, 0o777)
        create_timer()
        print("set alarm to false and create a new timer")
        return redirect(url_for('index'))

    return render_template('index.html', temp_week_ago=temp_week_ago, current_soiltemp=current_soiltemp,sensor1=sensor1, temp_difference=temp_difference,
                           temp_alarm=temp_alarm, temps=temps, soiltemps=soiltemps, dates=dates, current_time=current_time,
                           rows=rows, current_temp=current_temp, pin_status=pin_status, server_up="yes")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
