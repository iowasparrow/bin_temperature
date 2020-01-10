from flask import Flask, render_template, send_file, make_response, request, url_for
import sqlite3
import os
from werkzeug.utils import redirect
from datetime import datetime, timezone, timedelta
import createTable as createTable
import pprint
import socket

app = Flask(__name__)

alert_text_file = '/var/www/html/binweb/bin_temperature/alert_file.txt'
database = '/var/www/html/binweb/bin_temperature/sensorsData.db'


site_id = 1


def get_all(start_date='1900-01-01', end_date='2050-01-01'):  # this is for the chart
    conn = sqlite3.connect(database, check_same_thread=False)
    curs = conn.cursor()
    print("start date in getall function: " + start_date)
    print("end date in getall function: " + end_date)
    sql = "SELECT * FROM pidata WHERE timestamp >= ? AND timestamp <= ? ORDER BY timestamp DESC"
    curs.execute(sql, [start_date, end_date])
    data = curs.fetchall()
    dates = []
    airtemps = []
    soiltemps = []
    cputemps= []
    sensor1 = []
    sensor2 = []
    
    for row in reversed(data):
        dates.append(datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y %H:%M'))
        #topic
        airtemps.append(row[2])
        # siteids.append(row[3])
        soiltemps.append(row[4])
        #humidity5
        if row[6] is None or row[6] == 0: 
            # convert None to null so the chart is happy 
            cputemps.append('null') 
        else: 
            cputemps.append(row[6])

        if row[7] is None or row[7] == 0:
            # convert None to null so the chart is happy
            sensor1.append('null')
        else:
            sensor1.append(row[7])

        if row[8] is None or row[8] == 0 or row[8] == 185:
            # convert None to null so the chart is happy
            sensor2.append('null')
        else:
            sensor2.append(row[8])

            # sensor3.append(row[6])
        # sensor4.append(row[7])
        # sensor5.append(row[8])
        # sensor6.append(row[9])

    conn.close()
    return dates ,airtemps, soiltemps, cputemps, sensor1, sensor2


def get_all_old(start_date='1900-01-01', end_date='2050-01-01'):  # this is for the chart
    conn = sqlite3.connect(database, check_same_thread=False)
    curs = conn.cursor()
    print("start date in getall function: " + start_date)
    print("end date in getall function: " + end_date)
    sql = "SELECT * FROM DHT_data where temp <> 'None' AND timestamp >= ? AND timestamp <= ? ORDER BY timestamp DESC"
    curs.execute(sql, [start_date, end_date])
    data = curs.fetchall()
    dates = []
    temps = []
    # siteids = []
    soiltemps = []
    sensor1 = []
    sensor2 = []
    # sensor3 = []
    # sensor4 = []
    # sensor5 = []
    # sensor6 = []
    for row in reversed(data):
        dates.append(datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y %H:%M'))
        temps.append(row[3])
        # siteids.append(row[2])
        soiltemps.append(row[3])

        if row[4] is None or row[4] == 0:
            # convert None to null so the chart is happy
            sensor1.append('null')
        else:
            sensor1.append(row[4])

        if row[5] is None or row[5] == 0 or row[5] == 185:
            # convert None to null so the chart is happy
            sensor2.append('null')
        else:
            sensor2.append(row[5])

            # sensor3.append(row[6])
        # sensor4.append(row[7])
        # sensor5.append(row[8])
        # sensor6.append(row[9])

    conn.close()
    return dates, temps, soiltemps, sensor1, sensor2


@app.route("/reset", methods=['GET', 'POST'])
def something():
    createTable.reset()
    return "table was reset"


def number_records():  # display number of recoreds
    conn = sqlite3.connect(database, check_same_thread=False)
    curs = conn.cursor()
    curs.execute("SELECT COUNT (*) FROM pidata")
    datapoints = curs.fetchall()
    # print('\nTotal rows: {}'.format(datapoints[0][0]))
    conn.close()
    return datapoints[0][0]


def check_rapid_rise(current_temp, x):
    conn = sqlite3.connect(database, check_same_thread=False)
    curs = conn.cursor()
    temp_week_ago = 0
    for row in curs.execute(
            "SELECT * FROM pidata WHERE timestamp BETWEEN datetime('now', '-8 days') AND datetime('now', '-6 days') LIMIT 1;"):
        temp_week_ago = row[x]
    conn.close()
    if temp_week_ago is None:
        temp_week_ago = 0

    temp_difference = current_temp - temp_week_ago
    if temp_difference >= 3 and current_temp > 32:
        # print("DANGER RAPID RISE DETECTED 3 degrees in one week at 32.")
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
    # print(timer_start)
    now = datetime.now()
    timer_started = datetime.strptime(timer_start, '%Y-%m-%d %H:%M:%S.%f')
    delta = now - timer_started
    # fixed_delta = timedelta(hours=2)
    if delta > timedelta(hours=24):
        # print("timer function says cancel, timer enough time has passed")
        cancel = True
    else:
        # print("check timer function in timer modules returns false ")
        cancel = False

    # print(delta)
    # print('delta seconds=', delta.seconds)
    # print('delta days=', delta.days)
    return cancel


def set_temp_alarm(temp_alarm):  # we expect a string of true check status
    # alert_file = open("alert_file.txt", "w") # create the alert file
    if temp_alarm == 'true':
        if check_timer():
            if os.path.exists(alert_text_file):
                alert_file = open(alert_text_file, "rt")
                if alert_file.readline() == 'true':
                    alert_file.close()
                    # print("file contents=True close it and return true")
                    return 'true'
                else:
                    alert_file = open(alert_text_file, "w")
                    alert_file.write("true")
                    alert_file.close()
                    # print("file contents were overwritten")
                return 'true'
            else:
                alert_file = open(alert_text_file, "w")
                alert_file.write("true")
                alert_file.close()
                os.chmod(alert_text_file, 0o777)
                # print("File Created")

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
    sensor1 = []
    sensor2 = []
    for row in curs.execute("SELECT * FROM pidata ORDER BY timestamp DESC LIMIT 1"):
        current_time = str(row[0])
        current_temp = row[2]
        current_soiltemp = row[4]
        current_sensor1 = row[7]
        current_sensor2 = row[8]
    conn.close()

    # send current temp and databse row to check for rapid rise
    temp_difference, temp_week_ago = check_rapid_rise(current_temp, 2)
    temp_difference1, temp_week_ago1 = check_rapid_rise(current_sensor1, 7)
    temp_difference2, temp_week_ago2 = check_rapid_rise(current_sensor2, 8)

    return current_time, current_temp, temp_difference, temp_week_ago, current_soiltemp, current_sensor1, current_sensor2, temp_difference1, temp_week_ago1, temp_difference2, temp_week_ago2


@app.route("/", methods=['GET', 'POST'])
def index():
    x = "0"
    print("hello")
    if not request.values.get("aStartDate") and not request.values.get("aEndDate"):
        dates, temps, soiltemps, cputemps, sensor1, sensor2 = get_all()
    if request.values.get("aStartDate") and request.values.get("aEndDate"):
        start_date = request.values.get("aStartDate")
        end_date = request.values.get("aEndDate")
        dates, temps, soiltemps, cputemps, sensor1, sensor2 = get_all(start_date, end_date)
    if request.values.get("aStartDate") and not request.values.get("aEndDate"):
        start_date = request.values.get("aStartDate")
        dates, temps, soiltemps, cputemps, sensor1, sensor2 = get_all(start_date)
    if request.values.get("aEndDate") and not request.values.get("aStartDate"):
        end_date = request.values.get("aEndDate")
        dates, temps, soiltemps, cputemps, sensor1, sensor2 = get_all(x, end_date)

    current_time, current_temp, temp_difference, temp_week_ago, current_soiltemp, current_sensor1, current_sensor2, temp_difference1, temp_week_ago1, temp_difference2, temp_week_ago2 = get_current_data()
   

    rows = number_records()
    temp_alarm = set_temp_alarm("check_status")
    # pin_status = check_relay_status()
    pin_status = False

    if "clear_alarm" in request.form:
        # print("button pressed")
        alert_file = open(alert_text_file, "w")
        alert_file.write("false")
        alert_file.close()
        os.chmod(alert_text_file, 0o777)
        create_timer()
        # print("set alarm to false and create a new timer")
        return redirect(url_for('index'))

    return render_template('index.html', temp_week_ago=temp_week_ago, current_soiltemp=current_soiltemp,
                           sensor1=sensor1, sensor2=sensor2, temp_difference=temp_difference,
                           temp_difference1=temp_difference1, temp_week_ago1=temp_week_ago1,
                           temp_difference2=temp_difference2, temp_week_ago2=temp_week_ago2, temp_alarm=temp_alarm,
                           temps=temps, soiltemps=soiltemps, dates=dates, current_time=current_time, rows=rows,
                           current_temp=current_temp, cputemps=cputemps, pin_status=pin_status, current_sensor1=current_sensor1,
                           current_sensor2=current_sensor2, server_up="no")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
