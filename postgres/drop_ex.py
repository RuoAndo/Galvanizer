import sys 
import psycopg2

conn = psycopg2.connect(
    host = "127.0.0.1",
    port = 5432,
    database="sample",
    user="postgres",
    password="")

cur = conn.cursor()

try:
    sql = "drop TABLE ex;"
    cur.execute(sql)
    conn.commit()
except:
    print "drop TABLE ex failed"
    cur.close()
    conn.close()
