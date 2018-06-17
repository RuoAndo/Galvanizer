# -*- coding: utf-8 -*- 

import psycopg2
import numpy
import numpy as np

import sys 
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

argvs = sys.argv  
argc = len(argvs) 

dbname = argvs[1]
tblname = argvs[2]

connector4 = psycopg2.connect(host="127.0.0.1", database="realloc_2", user="postgres", password="")
connector4.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

try:
    cursor4 = connector4.cursor()
    sqlstr4 = "create table " + tblname + "(REALLOC_LINENUMBER INT NOT NULL, FUNCTION_NAME CHAR(50), FUNCTION_LINENUMBER CHAR(50));"
    print sqlstr4
    cursor4.execute(sqlstr4)
    connector4.commit
except:
    pass
    
connector = psycopg2.connect(host="127.0.0.1", database=dbname, user="postgres", password="")
connector.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = connector.cursor()

sqlstr = "select * from " + tblname
cursor.execute(sqlstr)

result = cursor.fetchall()

for row in result:

    #print row
    location = unicode(row[1]).rstrip(" ")
    #print location
    
    connector2 = psycopg2.connect(host="127.0.0.1", database=tblname, user="postgres", password="")
    connector2.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor2 = connector2.cursor()
    
    sqlstr2 = "select * from definition where location =" + "'" + location.rstrip(" ") + "';"

    #print sqlstr2
    
    #sqlstr2 = "select * from definition where location =" + "'" + "contrib/queryperf/queryperf.c" + "';"
    #sqlstr2 = "select * from definition where location =" + "'" + "lib/dns/acache.c" + "';"
    #sqlstr2 = "select * from definition;"

    cursor2.execute(sqlstr2)
    result2 = cursor2.fetchall()

    line_number_array = []
    for row2 in result2:
        try:
            line_number_array.append(int(unicode(row2[6])))
        except:
            pass

    #print line_number_array
        
    print "---------"
    line_number_array_uniq = list(set(line_number_array))
    x = np.sort(line_number_array_uniq).tolist()

    print "search:" + str(int(row[0]))
    print x
    y = np.searchsorted(x, int(row[0]), side='right')
    
    try:    
        caller_ln = str(x[y-1])
        callee_ln = str(int(row[0]))
    except:
        caller_ln = 0
        continue

    try:
        cursor3 = connector2.cursor()
        sql = "select * from definition where location =" + "'" + location + "' AND linenumber =" + "'" + str(x[y-1]) + "'"
        cursor3.execute(sql)
        result3 = cursor3.fetchall()
    except:
        continue

    #sql = "create TABLE test(id INT, function_name varchar(1024), location varchar(1024), linenumber INT);"
    #cursor2.execute(sqlstr4)
    
    for row3 in result3:
        print str(int(row[0])) + ":" + row3[4] + ":" + row3[5] + ":" + str(row3[6])

        connector5 = psycopg2.connect(host="127.0.0.1", database="realloc_2", user="postgres", password="")
        connector5.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor5 = connector4.cursor()

        sqlstr5 = "INSERT INTO " + tblname + "(REALLOC_LINENUMBER, FUNCTION_NAME, FUNCTION_LINENUMBER) VALUES (" + "'" + str(int(row[0])) + "'" + ", " + "'" + row3[4] + "'" + ", " + "'" + str(row3[6]) + "'" + ");" 
        print sqlstr5

        cursor5.execute(sqlstr5)
        connector5.commit
        
cursor.close()
connector.close()

