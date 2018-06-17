# create_callchain.py

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

cur2 = conn.cursor()

try:
    sql = "create TABLE callchain(id INT, software_version varchar(1024), listtype varchar(1024), function_name varchar(1024), location varchar(1024), linenumber INT);"
    cur2.execute(sql)
    conn.commit()

except:
    print "cur2 error"
    cur2.close()
    
conn.close()
