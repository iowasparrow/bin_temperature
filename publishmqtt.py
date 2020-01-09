#!/usr/bin/env python3
import requests
import paho.mqtt.client as mqtt
import tempSensor
import json
import sqlite3
# publish to broker and log to database

def read_sensor2():
    sensor2 = tempSensor.read_tempsensor2()
    (rc, mid) = client.publish("home/cathouse", sensor2, retain=True);
    return sensor2

def read_sensor1():
    sensor1 = tempSensor.read_tempsensor1()
    (rc, mid) = client.publish("home/hottub", sensor1, retain=True);
    return sensor1

def read_CPU():
    tempC = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3
    tempF = round((tempC * 9/5) + 32 ,2 )
    (rc, mid) = client.publish("home/cputemp", tempF, qos=1,retain=True);

def get_airtemp():
    pload = {}
    r = requests.get('http://mesonet.agron.iastate.edu/json/current.py?station=RIGI4&network=IA_RWIS', data=pload)
    x = r.json()
    #print(x['last_ob']['airtemp[F]'])
    airtemp = x['last_ob']['airtemp[F]']
    #print("got air temp= " + str(airtemp))
    return airtemp

def get_soiltemp():
    rsoil = {}
    rr = requests.get('http://mesonet.agron.iastate.edu/api/1/currents.json?network=ISUSM&station=BOOI4' , data=rsoil)
    xx = rr.json()
    soiltemp = xx['data'][0]['c2tmpf']
    #print(xx['data'][0]['c2tmpf'])
    print("got soil tempi= " + str(soiltemp))
    return soiltemp

def log_to_database(temp, soiltemp, sensor1, sensor2):
    fmt = "%Y-%m-%d %H:%M:%S"
    now_utc = datetime.now(timezone('UTC'))
    now_central = now_utc.astimezone(timezone('US/Central'))
    formatted_date = now_central.strftime(fmt)
    print("Formatted Date: " +formatted_date)
    conn = sqlite3.connect(dbname)
    curs = conn.cursor()
    curs.execute("INSERT INTO pidata VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (theTime, None, airtemp, None, soiltemp, None, sensor1, sensor2, None, None, None ,None ))
    conn.commit()
    conn.close()
    pass

def on_publish(client,userdata,mid):
    print("mid: "+str(mid))
    print("data published \n")
    pass

def on_connect(client, userdata, flags, rc):
    print("CONNACK received with code %d." % (rc))

client = mqtt.Client("raspberryPI")
client.on_connect = on_connect
client.on_publish = on_publish
client.connect("192.168.1.153",1883,60)
client.loop_start()

picpu = read_CPU()
sensor2 = read_sensor2()
sensor1 = read_sensor1()
client.loop_stop()
client.disconnect()

#airtemp = get_airtemp()
#soiltemp = get_soiltemp()
#log_to_database(picpu,sensor2,sensor1,airtemp,soiltemp)
