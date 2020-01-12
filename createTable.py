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
        print("function reset table")

def pidata():
    con = lite.connect(database)
    with con:
        cur = con.cursor()
        print("dropping table pidata if exists")
        cur.execute("DROP TABLE IF EXISTS pidata")
        cur.execute("CREATE TABLE pidata(timestamp DATETIME, topic TEXT, airtemp NUMERIC, siteid NUMERIC, soiltemp NUMERIC, humidity NUMERIC, picpu NUMERIC, sensor1 NUMERIC, sensor2 NUMERIC, sensor3 NUMERIC, sensor4 NUMERIC, sensor5 NUMERIC, sensor6 NUMERIC)")

def pitopic():
    con = lite.connect(database)
    with con:
        cur = con.cursor()
        print("dropping table pitopics if exists")
        cur.execute("DROP TABLE IF EXISTS pitopics")
        cur.execute("CREATE TABLE pitopics(timestamp DATETIME, topic TEXT, payload NUMERIC)")


def pihq():
    con = lite.connect(database)
    with con:
        cur = con.cursor()
        print("dropping table pihq")
        cur.execute("DROP TABLE IF EXISTS pihq")
        cur.execute("CREATE TABLE pihq(timestamp DATETIME, topic TEXT, airtemp NUMERIC, siteid NUMERIC, soiltemp NUMERIC, humidity NUMERIC, picpu NUMERIC, sensor1 NUMERIC, sensor2 NUMERIC, sensor3 NUMERIC, sensor4 NUMERIC, sensor5 NUMERIC, sensor6 NUMERIC)")


def create_timer():
    con = lite.connect(database)
    with con:
        cur = con.cursor()
        print("dropping table tbl_timer")
        cur.execute("DROP TABLE IF EXISTS tbl_timer")
        cur.execute("CREATE TABLE tbl_timer(timestamp DATETIME);")


create_timer()
pidata()
pihq()
pitopic()
