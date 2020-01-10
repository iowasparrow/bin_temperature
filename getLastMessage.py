import paho.mqtt.client as mqtt #import the client1
import time
############

#themess = 0

def on_message(client, userdata, message):
    #print("message received " ,str(message.payload.decode("utf-8")))
    yolo = str(message.payload.decode("utf-8"))
    print("Last Message: " + yolo )
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
    themess = yolo
    return yolo
########################################
broker_address="192.168.1.153"
#broker_address="test.mosquitto.org"

def getNewMessage(): 
    print("creating new instance")
    client = mqtt.Client("raspberry") #create new instance
    client.on_message=on_message #attach function to callback
    print("connecting to broker")
    client.connect(broker_address) #connect to broker
    client.loop_start() #start the loop
    print("Subscribing to topic","bigbin/tempsensor")
    client.subscribe("bigbin/tempsensor")
    #print("Publishing message to topic","house/bulbs/bulb1")
    #client.publish("house/bulbs/bulb1","ON")
    time.sleep(4) # wait
    client.loop_stop() #stop the loop
getNewMessage()

print(yolo)
