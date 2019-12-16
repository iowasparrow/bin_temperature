import json
import sqlite3
from datetime import datetime
from pytz import timezone
import requests
import time

#dbname = '/home/gsiebrecht/PycharmProjects/bin_temperature/sensorsData.db'
dbname = '/var/www/html/binweb/bin_temperature/sensorsData.db'
#dbname = 'sensorsData.db'
sampleFreq = 1500 # 2 hours
#  each site id is unique to the customer
siteid = 1


# get data from DHT sensor
def getDHTdata():
    pload = {}
    r = requests.post('http://mesonet.agron.iastate.edu/json/current.py?station=RIGI4&network=IA_RWIS', data=pload)
    x = r.json()
    #print(x['last_ob']['airtemp[F]'])
    temp = x['last_ob']['airtemp[F]']
    #print(x['last_ob']['airtemp[F]'])

    rsoil = {}
    rr = requests.post('http://mesonet.agron.iastate.edu/api/1/currents.json?network=ISUSM&station=BOOI4' , data=rsoil)
    xx = rr.json()
    #print(type(rr.json())) #shows type as a dict
    #print(xx)
    soiltemp = xx['data'][0]['c2tmpf']
    print(xx['data'][0]['c2tmpf'])
    print("END API")
    return temp, soiltemp


# log sensor data on database
def logData(temp, soiltemp):
    fmt = "%Y-%m-%d %H:%M:%S"
    now_utc = datetime.now(timezone('UTC'))
    now_central = now_utc.astimezone(timezone('US/Central'))
    #print(now_central.strftime(fmt))
    formatted_date = now_central.strftime(fmt)
    #print(formatted_date)
    conn = sqlite3.connect(dbname)
    curs = conn.cursor()
    curs.execute("INSERT INTO DHT_data values((?), (?),  (?),  (?),  (?),  (?),  (?),  (?), (?), (?))", (formatted_date, temp, siteid, soiltemp, 0,0,0,0,0,0))
    conn.commit()
    conn.close()
    sensor1 = 0
    sensor2 = 0
    send_data_to_api(temp,soiltemp, sensor1, sensor2)

def send_data_to_api(temp,soiltemp,sensor1,sensor2):
    url = 'http://bintemp.com/binapi/api/v1.0/tasks'
    payload = {"temp": temp, "siteid": siteid, "soiltemp": soiltemp, "sensor1":sensor1, "sensor2":sensor2}
    headers = {'content-type': 'application/json'}
    print(url)
    print(payload)
    print(headers)
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    print("This is the Send To API Function")
    print(json.dumps(payload))
    print(json.dumps(headers))
    return response



# display database data
def displayData():
    conn = sqlite3.connect(dbname)
    curs = conn.cursor()
    print("\nEntire database contents:\n")
    for row in curs.execute("SELECT * FROM DHT_data"):
        print(row)
    conn.close()


# main function
def main():
#    while True:
        temp, soiltemp = getDHTdata()
        logData(temp, soiltemp)
        displayData()
        #print("sleeping")
        #time.sleep(sampleFreq)



# Execute program
main()
