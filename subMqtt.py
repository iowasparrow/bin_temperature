#!/usr/bin/python3
import sqlite3
import paho.mqtt.client as mqtt
from datetime import datetime
from pytz import timezone

dbname = '/var/www/html/binweb/bin_temperature/sensorsData.db'

def log_to_database(sensor6):
    fmt = "%Y-%m-%d %H:%M:%S"
    now_utc = datetime.now(timezone('UTC'))
    now_central = now_utc.astimezone(timezone('US/Central'))
    #print("time now in appdht:" + now_central.strftime(fmt))
    formatted_date = now_central.strftime(fmt)
    conn = sqlite3.connect(dbname)
    curs = conn.cursor()
    curs.execute("INSERT INTO DHT_data values((?), (?),  (?),  (?),  (?),  (?),  (?), (?),(?), (?))", (formatted_date, None, None, None, None, None ,None, None, None, sensor6))
    conn.commit()
    conn.close()



# This is the Subscriber

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("home/hottub")

def on_message(client, userdata, msg):
    #if msg.payload.decode() == "Hello world!":
    #print("Yes!")
    themessage = msg.payload.decode()
    log_to_database(themessage)
    print(themessage)
    #client.disconnect()
    
client = mqtt.Client()
client.connect("192.168.1.153",1883,60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()
