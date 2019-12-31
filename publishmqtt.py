#!/usr/bin/env python3

import paho.mqtt.client as mqtt

# This is the Publisher

def publish_message():
    client = mqtt.Client()
    client.connect("192.168.1.153",1883,60)
    client.publish("home/hottub", "32",retain=True);
    client.disconnect();

publish_message()
