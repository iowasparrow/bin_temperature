import sqlite3
from datetime import datetime, timezone, timedelta
database = 'sensorsData.db'

def create_timer():
    conn = sqlite3.connect(database)
    curs = conn.cursor()
    timestamp = datetime.now()
    curs.execute("INSERT INTO tbl_timer values((?))", (timestamp,))
    conn.commit()
    conn.close()

def check_timer():
    conn = sqlite3.connect(database)
    curs = conn.cursor()
    timer_start = []
    for row in curs.execute("SELECT * FROM tbl_timer"):
        timer_start = row[0]
    conn.close()
    #print(timer_start)
    now = datetime.now()
    timer_started = datetime.strptime(timer_start, '%Y-%m-%d %H:%M:%S.%f')
    delta = now - timer_started
    fixed_delta = timedelta(seconds=8000)  #2.22 hours
    if delta > fixed_delta:
        print("timer function says cancel timer enough time has passed")
        cancel = True
    else:
        print("check timer function in timer modules returns false ")
        cancel = False

    #print(delta)
    #print('delta seconds=', delta.seconds)
    #print('delta days=', delta.days)
    return cancel


#dif = check_timer()
#print(dif)