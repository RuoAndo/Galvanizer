# callchains.py

# libxl_domain_rename:rc = libxl_domain_rename(ctx, domid, info->name, preserved_name, t);:libxl.c:306
# sprintf:return sprintf(buf, "%d\n", DIV_FROM_REG(data->fan_div[attr->index]));:drivers/hwmon/smsc47m1.c:240

# sql = "create TABLE test(id INT, software_version varchar(1024), linktype varchar(1024), function_name varchar(1024), location varchar(1024), linenumber INT);"

#1 id : 1 
#2 software_version : bind998
#3 listtype : callchain
#5 function_name : libxl_string_list_destroy(libxl_string_list *psl)
#6 location : drivers/hwmon/smsc47m1.c
#7 linenumber : 240

import sys 
import psycopg2

argvs = sys.argv  
argc = len(argvs) 

f = open(argvs[1])
software_version = argvs[2]
dbname = argvs[2]

conn = psycopg2.connect(
    host = "127.0.0.1",
    port = 5432,
    database=dbname,
    user="postgres",
    password="")

cur = conn.cursor()
    
f = open(argvs[1])

counter = 0
line = f.readline() 
while line:

    tmp = line.split(":")

    print line
    listtype = "callchain"
    function_name = tmp[0]
    location = tmp[2]
    linenumber = tmp[3].strip()
    
    print "#### INSERT ####"
    print "function_name:" + function_name
    print "location:" + location
    print "linenumber:" + linenumber
    print "software_version:" + software_version
    print "listtype: callchain"
    print "####        ####"
    
    print "isDigit:" + tmp[3].strip() + ":" + str(tmp[3].strip().isdigit())

    if line.find('ifdef') == -1:

        if tmp[3].strip().isdigit():
            
            sql = "INSERT INTO callchain (id, software_version, listtype, function_name, location, linenumber) VALUES (" + str(counter) + ", '" + software_version
            #print sql

            sql = sql + "', '" + listtype
            #print sql

            sql = sql + "', '" + function_name
            #print sql

            sql = sql + "', '" + location
            #print sql

            sql = sql + "', " + linenumber + ");"
            print sql
            
            cur.execute(sql)
            conn.commit()
                
    counter=counter + 1
    line = f.readline() 

cur.close()
conn.close()
