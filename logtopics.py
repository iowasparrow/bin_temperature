#!/usr/bin/env python3
from time import gmtime, strftime
import paho.mqtt.client as mqtt
import sqlite3
import time
from datetime import datetime
from pytz import timezone

sensor2_topic = "home/cathouse"
sensor1_topic = "home/hottub"
airtemp_topic = "home/airtemp"
soiltemp_topic = "home/soiltemp"
picpu_topic = "home/cputemp"
crash_picpu_topic = "crash/cputemp"

dbname = '/var/www/html/binweb/bin_temperature/sensorsData.db'

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(sensor1_topic)
    client.subscribe(sensor2_topic)
    client.subscribe(airtemp_topic)
    client.subscribe(soiltemp_topic)
    client.subscribe(picpu_topic)
    client.subscribe(crash_picpu_topic)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    fmt = "%Y-%m-%d %H:%M:%S"
    now_utc = datetime.now(timezone('UTC'))
    now_central = now_utc.astimezone(timezone('US/Central'))
    theTime = now_central.strftime(fmt)
    #theTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    result = (theTime + "\t" + str(msg.payload))
    print(msg.topic + ":\t" + result)

    mypayload = msg.payload.decode()
    mytopic = msg.topic 

    writeToDb(theTime, mytopic, mypayload)
    return

def writeToDb(theTime, mytopic, mypayload):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    print("Writing to db...")
    c.execute("INSERT INTO pitopics VALUES (?,?,?)", (theTime, mytopic, mypayload ))
    
    conn.commit()

    #global dataTuple
    #dataTuple = [-1, -1]
print("sleeping 3 seconds, two cron jobs are scheduled on the minute.")
time.sleep(3)

client = mqtt.Client()
try:
    print("trying to connect, will try for 30 seconds")
    #client.connect("192.168.1.153", 1883, 60)
    client.connect("bintemp.com",1883 , 60)
    client.loop_start()
except:
    print("can't reach the broker")
    exit(1)

client.on_connect = on_connect
print("connecting to broker")
client.on_message = on_message
print("waiting for messages")
time.sleep(5)
client.loop_stop()



# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
#client.loop_forever()
#client.loop_start()

