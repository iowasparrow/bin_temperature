#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import tempSensor
# This is the Publisher

def read_sensor2():
    temp = tempSensor.read_tempsensor2()
    (rc, mid) = client.publish("home/cathouse", temp, retain=True);

def read_sensor1():
    sensor1 = tempSensor.read_tempsensor1()
    (rc, mid) = client.publish("home/hottub", sensor1, retain=True);


def readCPU():
    tempC = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3
    tempF = round((tempC * 9/5) + 32 ,2 )
    #client = mqtt.Client()
    #client.connect("192.168.1.153",1883,60)
    (rc, mid) = client.publish("home/cputemp", tempF, qos=1,retain=True);
    
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

readCPU()
read_sensor2()
read_sensor1()
client.disconnect()
