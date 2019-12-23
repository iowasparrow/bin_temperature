import sqlite3 as lite


#database = '/home/gsiebrecht/PycharmProjects/bin_temperature/sensorsData.db'
database = 'sensorsData.db'

def reset():
    con = lite.connect(database)
    with con:
        cur = con.cursor()
        cur.execute("DELETE FROM DHT_data WHERE timestamp <= date('now','-365 day')")
        print("Old Data Deleted")
reset()
