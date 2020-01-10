#!/usr/bin/env python3 
import sqlite3
import paho.mqtt.client as mqtt
from datetime import datetime
from pytz import timezone

dbname = '/var/www/html/binweb/bin_temperature/sensorsData.db'

# This is the Subscriber

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("home/hottub")

def on_message(client, userdata, msg):
    themessage = msg.payload.decode()
    topic = msg.topic
    print(topic)
    print(themessage)
    #client.disconnect()
    
client = mqtt.Client()
client.connect("192.168.1.153",1883,60)

client.on_connect = on_connect
client.on_message = on_message
client.loop_forever()
