import json
import sqlite3
from datetime import datetime
from pytz import timezone
import requests
import time
import subprocess
import tempSensor
#import publishmqtt
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
#from tempSensor import read_temp

dbname = '/var/www/html/binweb/bin_temperature/sensorsData.db'
sampleFreq = 1500 # 2 hours
#  each site id is unique to the customer
siteid = 1

#cmd = "cat" ,"/sys/devices/virtual/thermal/thermal_zone0/temp"


# get data from DHT sensor
def getDHTdata():
    print("starting to get air temp")
    pload = {}
    r = requests.get('http://mesonet.agron.iastate.edu/json/current.py?station=RIGI4&network=IA_RWIS', data=pload)
    x = r.json()
    #print(x['last_ob']['airtemp[F]'])
    temp = x['last_ob']['airtemp[F]']
    print("got air temp")

    rsoil = {}
    rr = requests.get('http://mesonet.agron.iastate.edu/api/1/currents.json?network=ISUSM&station=BOOI4' , data=rsoil)
    xx = rr.json()
    soiltemp = xx['data'][0]['c2tmpf']
    #print(xx['data'][0]['c2tmpf'])
    print("got soil temp")
    
    #client = mqtt.Client()
    #client.connect("192.168.1.153",1883,60);
    #client.publish("home/airtemp", temp, retain=True)
    #publish.single("home/airtemp", temp, retain=True, hostname="192.168.1.153", port=1883)
    #client.disconnect()
    
    #client = mqtt.Client()
    #client.connect("192.168.1.153",1883,60);
    #time.sleep(.2)
    #publish.single("home/soiltemp", soiltemp, retain=True, hostname="192.168.1.153", port=1883)
    #client.disconnect()


    #client = mqtt.Client()
    #client.connect("192.168.1.153",1883,60);
    #client.publish("home/airtemp", temp, retain=True)
    #client.publish("home/soiltemp", temp, retain=True)
    #client.disconnect()

    


    sensor1 = tempSensor.read_tempsensor1()
    sensor2 = tempSensor.read_tempsensor2()    
    return temp, soiltemp, sensor1, sensor2


# log sensor data on database
def logData(temp, soiltemp, sensor1, sensor2):
    fmt = "%Y-%m-%d %H:%M:%S"
    now_utc = datetime.now(timezone('UTC'))
    now_central = now_utc.astimezone(timezone('US/Central'))
    formatted_date = now_central.strftime(fmt)
    print("Formatted Date in appdht: " +formatted_date)
    conn = sqlite3.connect(dbname)
    curs = conn.cursor()
    curs.execute("INSERT INTO DHT_data values((?), (?),  (?),  (?),  (?),  (?),  (?), (?),(?), (?))", (formatted_date, temp, siteid, soiltemp, sensor1, sensor2 ,None, None, None, None))
    conn.commit()
    conn.close()
    send_data_to_api(temp, soiltemp, sensor1, sensor2)

def send_data_to_api(temp,soiltemp,sensor1,sensor2):
    url = 'http://bintemp.com/binapi/api/v1.0/tasks'
    payload = {"temp": temp, "siteid": siteid, "soiltemp": soiltemp, "sensor1":sensor1, "sensor2":sensor2}
    headers = {'content-type': 'application/json'}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    print("This is the Send To API Function")
    print(json.dumps(payload))
    print(json.dumps(headers))
    #publishmqtt.publish_message(sensor1)
    #publishmqtt.readCPU()
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
        temp, soiltemp, sensor1, sensor2 = getDHTdata()
        logData(temp, soiltemp, sensor1, sensor2)
        #publishmqtt.publish_message
        #print("mqtt sensor=" + simple.getmessage())        
        #displayData()
        #print("sleeping")
        #time.sleep(sampleFreq)



# Execute program
main()
