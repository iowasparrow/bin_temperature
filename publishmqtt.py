#!/usr/bin/env python3

import paho.mqtt.client as mqtt

# This is the Publisher

def publish_message(temp):
    client = mqtt.Client()
    client.connect("192.168.1.153",1883,60)
    client.publish("home/hottub", temp ,retain=True);
    client.disconnect();
    
def readCPU():
    tempC = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3
    tempF = (tempC * 9/5) + 32
    client = mqtt.Client()
    client.connect("192.168.1.153",1883,60)
    client.publish("home/cputemp", tempF ,retain=True);
    client.disconnect();
    
    #print(tempF)

#readCPU()

#publish_message()
