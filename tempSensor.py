import os
import time

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

sensor_1 = '/sys/bus/w1/devices/28-00000b91fb79/w1_slave'


#def read_temp_raw():
#    f = open(temp_sensor, 'r')
#    lines = f.readlines()
#    f.close()
#    return lines


def read_tempsensor1():
    f = open(sensor_1, 'r')
    lines = f.readlines()
    f.close()
#    lines = read_temp_raw()
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
#while True:
print(read_tempsensor1())
#    time.sleep(1)
