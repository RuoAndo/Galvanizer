import sys 
import psycopg2

argvs = sys.argv  
argc = len(argvs) 

dbname = argvs[1]

conn = psycopg2.connect(
    host = "127.0.0.1",
    port = 5432,
    database=dbname,
    user="postgres",
    password="")

cur = conn.cursor()

try:
    sql = "drop TABLE definition;"
    cur.execute(sql)
    conn.commit()
except:
    print "drop TABLE definition failed"
    cur.close()
    conn.close()
