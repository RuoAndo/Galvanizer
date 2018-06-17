import sys 
import psycopg2

argvs = sys.argv  
argc = len(argvs) 

dbname = argvs[1]
tablename = argvs[2]

conn = psycopg2.connect(
    host = "127.0.0.1",
    port = 5432,
    database=dbname,
    user="postgres",
    password="")

cur = conn.cursor()

sql = "select count(*) from " + tablename + ";"
cur.execute(sql)
(number_of_row, ) = cur.fetchone()
print number_of_row

#stats = cur.fetchall()
#out =  str(stats)

#sql = "select count(*) from callchain;"
#cur.execute(sql)

#stats = cur.fetchall()
#out = out + str(stats)

#sql = "select count(*) from ex;"
#cur.execute(sql)

#stats = cur.fetchall()
#out = out + str(stats)
#print out
