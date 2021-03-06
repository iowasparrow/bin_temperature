#!/usr/bin/env python3
import requests
import paho.mqtt.client as mqtt
import tempSensor
import json
import sqlite3
from datetime import datetime
from pytz import timezone
from time import sleep
import random

dbname = '/var/www/html/binweb/bin_temperature/sensorsData.db'
siteid = 3 
#sleep becasue we have other cron jobs startin at the same time
sleep(random.randrange(3,10))


# publish to broker and log to database

def read_sensor2():
    sensor2 = tempSensor.read_tempsensor2()
    return sensor2

def read_sensor1():
    sensor1 = tempSensor.read_tempsensor1()
    return sensor1

def read_CPU():
    tempC = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3
    tempF = round((tempC * 9/5) + 32 ,2 )
    return tempF

def get_airtemp():
    pload = {}
    r = requests.get('http://mesonet.agron.iastate.edu/json/current.py?station=RIGI4&network=IA_RWIS', data=pload)
    x = r.json()
    #print(x['last_ob']['airtemp[F]'])
    airtemp = x['last_ob']['airtemp[F]']
    #print("got air temp= " + str(airtemp))
    #(rc, mid) = client.publish("home/airtemp", airtemp, qos=1,retain=True);
    return airtemp

def get_soiltemp():
    rsoil = {}
    rr = requests.get('http://mesonet.agron.iastate.edu/api/1/currents.json?network=ISUSM&station=BOOI4' , data=rsoil)
    xx = rr.json()
    soiltemp1 = xx['data'][0]['c2tmpf']
    soiltemp = round(soiltemp1,2)
    #(rc, mid) = client.publish("home/soiltemp", soiltemp, qos=1,retain=True);
    #print(xx['data'][0]['c2tmpf'])
    #print("got soil temp= " + str(soiltemp))
    return soiltemp

def send_data_to_api(siteid, sensor2, sensor1, airtemp, soiltemp, picpu):
    """ send data to remote pi for logging into pihq database"""
    url = 'http://bintemp.com/binapi/api/insert' 
    payload = {"airtemp": airtemp, "siteid": siteid, "soiltemp": soiltemp, "sensor1":sensor1, "sensor2":sensor2, "picpu": picpu} 
    headers = {'content-type': 'application/json'} 
    response = requests.post(url, data=json.dumps(payload), headers=headers) 
    #print("siteid = " + str(siteid))
    #print(json.dumps(payload)) 
    #print(json.dumps(headers)) 
    return response

def log_to_database(siteid,sensor2,sensor1,airtemp,soiltemp,picpu):
    """ log to local table (pidata) """
    fmt = "%Y-%m-%d %H:%M:%S"
    now_utc = datetime.now(timezone('UTC'))
    now_central = now_utc.astimezone(timezone('US/Central'))
    formatted_date = now_central.strftime(fmt)
    #print("Formatted Date: " +formatted_date)
    conn = sqlite3.connect(dbname)
    curs = conn.cursor()
    curs.execute("INSERT INTO pidata VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", (formatted_date, None, airtemp, siteid, soiltemp, None, picpu, sensor1, sensor2, None, None, None ,None ))
    conn.commit()
    conn.close()

def on_publish(client,userdata,mid):
    print("mid: "+str(mid))
    print("data published \n")
    pass

def on_connect(client, userdata, flags, rc):
    print("CONNACK received with code %d." % (rc))

#client = mqtt.Client("raspberryPI")
#client.on_connect = on_connect
#client.on_publish = on_publish
#client.connect("192.168.1.153",1883,60)
#client.loop_start()

def sendtobroker(picpu,sensor1,sensor2,airtemp,soiltemp):
    client = mqtt.Client("raspberryPI")
    client.on_connect = on_connect
    client.on_publish = on_publish
    try:
        print("trying the broker")
        client.connect("192.168.1.153",1883,60)
        #client.connect("192.168.9.100",1883,60)
    except:
        print("connection failed can not reach the broker")
        exit(1)
    client.loop_start()
#    (rc, mid) = client.publish("home/cputemp", picpu, qos=1,retain=True);
    (rc, mid) = client.publish("home/bintemp/sparesensor", sensor1, retain=True);
#    (rc, mid) = client.publish("home/bintemp/sensor2", sensor2, retain=True);
#    (rc, mid) = client.publish("home/airtemp", airtemp, qos=1,retain=True);
#    (rc, mid) = client.publish("home/soiltemp", soiltemp, qos=1,retain=True);
    client.loop_stop()
    client.disconnect()


try:
    sensor1 = read_sensor1()
except:
    sensor1 = None

try:
    sensor2 = read_sensor2()
except:
    sensor2 = None


picpu = read_CPU()
airtemp = get_airtemp()
soiltemp = get_soiltemp()


print("logging to database first, in case the broker is down.")
#log_to_database(siteid,sensor2,sensor1,airtemp,soiltemp,picpu)
print("done logging to database")

try:
    send_data_to_api(siteid,sensor2,sensor1,airtemp,soiltemp,picpu)
except:
    print("cannot find the api server, will try the broker for the next 30 seconds")

sendtobroker(picpu,sensor1,sensor2,airtemp,soiltemp)


#sensor2 = read_sensor2()
#sensor1 = read_sensor1()
#airtemp = get_airtemp()
#soiltemp = get_soiltemp()

#client.loop_stop()
#client.disconnect()
