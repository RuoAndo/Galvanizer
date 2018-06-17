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

conn = psycopg2.connect(
    host = "127.0.0.1",
    port = 5432,
    database=dbname,
    user="postgres",
    password="")

cur = conn.cursor()

sql = "create TABLE definition(id INT, software_version varchar(1024), listtype varchar(1024), function_type varchar(1024), function_name varchar(1024), location varchar(1024), linenumber INT);"
cur.execute(sql)
conn.commit()

conn.close()
