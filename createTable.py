import sqlite3 as lite


#database = '/home/gsiebrecht/PycharmProjects/bin_temperature/sensorsData.db'
database = 'sensorsData.db'

def reset():
    con = lite.connect(database)
    with con:
        cur = con.cursor()
        print("dropping table")
        cur.execute("DROP TABLE IF EXISTS DHT_data")
        cur.execute("CREATE TABLE DHT_data(timestamp DATETIME, temp NUMERIC, siteid NUMERIC, soiltemp NUMERIC, sensor1 NUMERIC, sensor2 NUMERIC, sensor3 NUMERIC, sensor4 NUMERIC, sensor5 NUMERIC, sensor6 NUMERIC)")
        #cur.execute("CREATE TABLE tbl_timer(timestamp DATETIME)")
        print("function reset table")
#reset()

def pidata():
    con = lite.connect(database)
    with con:
        cur = con.cursor()
        print("dropping table pidata if exists")
        cur.execute("DROP TABLE IF EXISTS pidata")
        cur.execute("CREATE TABLE pidata(timestamp DATETIME, topic TEXT, airtemp NUMERIC, siteid NUMERIC, soiltemp NUMERIC, humidity NUMERIC, picpu NUMERIC, sensor1 NUMERIC, sensor2 NUMERIC, sensor3 NUMERIC, sensor4 NUMERIC, sensor5 NUMERIC, sensor6 NUMERIC)")
pidata()

def pihq():
    con = lite.connect(database)
    with con:
        cur = con.cursor()
        print("dropping table pihq")
        cur.execute("DROP TABLE IF EXISTS pihq")
        cur.execute("CREATE TABLE pihq(timestamp DATETIME, topic TEXT, airtemp NUMERIC, siteid NUMERIC, soiltemp NUMERIC, humidity NUMERIC, picpu NUMERIC, sensor1 NUMERIC, sensor2 NUMERIC, sensor3 NUMERIC, sensor4 NUMERIC, sensor5 NUMERIC, sensor6 NUMERIC)")
pihq()

