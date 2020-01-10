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

dbname = '/var/www/html/binweb/bin_temperature/sensorsData.db'

dataTuple = [-1,-1,-1,-1,-1]

client = mqtt.Client()
client.connect("192.168.1.153", 1883, 60)
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(sensor1_topic)
    client.subscribe(sensor2_topic)
    client.subscribe(airtemp_topic)
    client.subscribe(soiltemp_topic)
    client.subscribe(picpu_topic)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    fmt = "%Y-%m-%d %H:%M:%S"
    now_utc = datetime.now(timezone('UTC'))
    now_central = now_utc.astimezone(timezone('US/Central'))
    theTime = now_central.strftime(fmt)
    #theTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    #print(theTime)

    #theTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    result = (theTime + "\t" + str(msg.payload))
    print(msg.topic + ":\t" + result)

    if (msg.topic == sensor1_topic):
        dataTuple[0] = msg.payload.decode()
    if (msg.topic == sensor2_topic): 
        dataTuple[1] = msg.payload.decode()
    if (msg.topic == airtemp_topic): 
        dataTuple[2] = msg.payload.decode()
    if (msg.topic == soiltemp_topic): 
        dataTuple[3] = msg.payload.decode()
    if (msg.topic == picpu_topic):
        dataTuple[4] = msg.payload.decode()
        #return
    
    if (dataTuple[0] != -1 and dataTuple[1] != -1 and dataTuple[2] != -1 and dataTuple[3] != -1 and dataTuple[4] != -1):
        writeToDb(theTime, dataTuple[0], dataTuple[1], dataTuple[2], dataTuple[3], dataTuple[4])
    return

def writeToDb(theTime, sensor1, sensor2, airtemp, soiltemp, picpu):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    print("Writing to db...")
    c.execute("INSERT INTO pihq VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", (theTime, None, airtemp, None, soiltemp, None, picpu, sensor1, sensor2, None, None, None ,None ))
    
    conn.commit()

    #global dataTuple
    #dataTuple = [-1, -1]
print("sleeping 15 seconds, wait for the cron job to do its thing in case they fire at the same time")
time.sleep(15)
client = mqtt.Client()
client.connect("192.168.1.153", 1883, 60)
client.loop_start()
client.on_connect = on_connect
print("connecting to broker")
client.on_message = on_message
print("waiting for messages")
time.sleep(10)
client.loop_stop()



# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
#client.loop_forever()
#client.loop_start()
