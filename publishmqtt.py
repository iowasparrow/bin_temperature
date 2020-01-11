#!/usr/bin/env python3
import requests
import paho.mqtt.client as mqtt
import tempSensor
import json
import sqlite3
from datetime import datetime
from pytz import timezone

dbname = '/var/www/html/binweb/bin_temperature/sensorsData.db'
siteid = 1
# publish to broker and log to database

def read_sensor2():
    sensor2 = tempSensor.read_tempsensor2()
    #(rc, mid) = client.publish("home/cathouse", sensor2, retain=True);
    return sensor2

def read_sensor1():
    sensor1 = tempSensor.read_tempsensor1()
    #(rc, mid) = client.publish("home/hottub", sensor1, retain=True);
    return sensor1

def read_CPU():
    tempC = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3
    tempF = round((tempC * 9/5) + 32 ,2 )
    #(rc, mid) = client.publish("home/cputemp", tempF, qos=1,retain=True);
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
    url = 'http://bintemp.com/binapi/api/insert' 
    payload = {"airtemp": airtemp, "siteid": siteid, "soiltemp": soiltemp, "sensor1":sensor1, "sensor2":sensor2, "picpu": picpu} 
    headers = {'content-type': 'application/json'} 
    response = requests.post(url, data=json.dumps(payload), headers=headers) 
    print(siteid)
    print(json.dumps(payload)) 
    print(json.dumps(headers)) 
    #publishmqtt.publish_message(sensor1) 
    #publishmqtt.readCPU() 
    return response

def log_to_database(siteid,sensor2,sensor1,airtemp,soiltemp,picpu):
    fmt = "%Y-%m-%d %H:%M:%S"
    now_utc = datetime.now(timezone('UTC'))
    now_central = now_utc.astimezone(timezone('US/Central'))
    formatted_date = now_central.strftime(fmt)
    #print("Formatted Date: " +formatted_date)
    conn = sqlite3.connect(dbname)
    curs = conn.cursor()
    curs.execute("INSERT INTO pidata VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", (formatted_date, siteid, airtemp, None, soiltemp, None, picpu, sensor1, sensor2, None, None, None ,None ))
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

def sendtobroker(tempF,sensor1,sensor2,airtemp,soiltemp):
    client = mqtt.Client("raspberryPI")
    client.on_connect = on_connect
    client.on_publish = on_publish
    try:
        client.connect("192.168.1.153",1883,60)
        #client.connect("192.168.9.102",1883,60)
    except:
        print("connection failed cannt reach the broker")
        exit(1)
    client.loop_start()
    (rc, mid) = client.publish("home/cputemp", tempF, qos=1,retain=True);
    (rc, mid) = client.publish("home/hottub", sensor1, retain=True);
    (rc, mid) = client.publish("home/cathouse", sensor2, retain=True);
    (rc, mid) = client.publish("home/airtemp", airtemp, qos=1,retain=True);
    (rc, mid) = client.publish("home/soiltemp", soiltemp, qos=1,retain=True);
    client.loop_stop()
    client.disconnect()


sensor1 = read_sensor1()
sensor2 = read_sensor2()
picpu = read_CPU()
airtemp = get_airtemp()
soiltemp = get_soiltemp()


print("logging to database first, in case the broker is down.")
log_to_database(siteid,sensor2,sensor1,airtemp,soiltemp,picpu)
send_data_to_api(siteid,sensor2,sensor1,airtemp,soiltemp,picpu)

sendtobroker(picpu,sensor1,sensor2,airtemp,soiltemp)


#sensor2 = read_sensor2()
#sensor1 = read_sensor1()
#airtemp = get_airtemp()
#soiltemp = get_soiltemp()

#client.loop_stop()
#client.disconnect()
