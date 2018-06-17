# inserting callchains
# libxl_domain_rename:rc = libxl_domain_rename(ctx, domid, info->name, preserved_name, t);:libxl.c:306
# xcinfo2xlinfo:xcinfo2xlinfo(&info[i], &ptr[i]);:Saturator-14/libxl.c:366
# libxl_domain_info:if (libxl_domain_info(ctx, info, domid) < 0):Saturator-14/libxl.c:609

import sys 
import psycopg2

conn = psycopg2.connect(
    host = "192.168.1.1",
    port = 5432,
    database="sample",
    user="postgres",
    password="")

cur = conn.cursor()

sql = "drop TABLE test;"
cur.execute(sql)

#sql = "create TABLE test(id INT, name varchar(1024));"
#sql = "create TABLE test(id INT, function_name varchar(1024));"
sql = "create TABLE test(id INT, function_name varchar(1024), location varchar(1024), linenumber INT);"
cur.execute(sql)

argvs = sys.argv  
argc = len(argvs) 

f = open(argvs[1])

counter = 0
line = f.readline() 
while line:

    tmp = line.split(":")

    print line
    print "function_name:" + tmp[0]
    print "location:" + tmp[2]
    print "linenumber:" + tmp[3]

    print "isDigit:" + tmp[3].strip() + ":" + str(tmp[3].strip().isdigit())
    
    if line.find('ifdef') == -1:

        if tmp[3].strip().isdigit():        
            sql = "INSERT INTO test (id, function_name, location, linenumber) VALUES (" + str(counter) + ", '" + tmp[0] + "', '" + tmp[2] + "', '" + tmp[3] + "');"
    
            print sql
            cur.execute(sql)

            
    counter=counter + 1
    line = f.readline() 

conn.commit()
cur.close()
conn.close()
