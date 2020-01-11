import os
import time
from os import path

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

#sensor_1 = '/sys/bus/w1/devices/28-0000035b0c33/w1_slave'
sensor_2 = '/sys/bus/w1/devices/10-00080235182a/w1_slave'
sensor_1 = '/sys/bus/w1/devices/28-00000b91fb79/w1_slave'


#print ("sensor one exist: "+str(path.exists(sensor_1)))
#print ("sensor two exist: "+str(path.exists(sensor_2)))




def read_tempsensor1():
    
    if (path.exists(sensor_1)):

        f = open(sensor_1, 'r')
    
        lines = f.readlines()
        f.close()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos + 2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            #return temp_c, temp_f
            rounded_temp =  round(temp_f, 2)
            return float(rounded_temp)
    else:
        return(0)
#print("sensor1")
#print(read_tempsensor1())

def read_tempsensor2():

    if (path.exists(sensor_2)):

        f = open(sensor_2, 'r')

        lines = f.readlines()
        f.close()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos + 2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            #return temp_c, temp_f
            rounded_temp =  round(temp_f, 2)
            return float(rounded_temp)
    else:
        return(0)


#print("sensor1")
#print(read_tempsensor1())

#print("sensor2")
#print(read_tempsensor2())
