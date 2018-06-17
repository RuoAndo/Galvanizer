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

sql = "create TABLE ex(id INT, software_version varchar(1024), caller_name varchar(1024), caller_linenumber INT, callee_name varchar(1024), callee_linenumber INT, location varchar(1024));"
cur.execute(sql)
conn.commit()

conn.close()
