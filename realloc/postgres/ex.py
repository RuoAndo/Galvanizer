# -*- coding: utf-8 -*- 

import psycopg2
import numpy
import numpy as np

import sys 
import psycopg2

argvs = sys.argv  
argc = len(argvs) 

software_version = argvs[1]
dbname = argvs[1]

connector = psycopg2.connect(host="127.0.0.1", database=dbname, user="postgres", password="")
cursor = connector.cursor()
cursor.execute("select * from callchain")

#result = cursor.fetchmany(20)
result = cursor.fetchall()

for row in result:

    location = unicode(row[4])
    #print "location -- " + unicode(row[4])

    linenumber = int(unicode(row[5]))
    #print "linenumber -- " + unicode(row[5])

    #print unicode(row[3]) + ":" + unicode(row[4]) + ":" + unicode(row[5])
    str_callchain = unicode(row[3]) + ":" + unicode(row[4]) + ":" + unicode(row[5])

    cursor2 = connector.cursor()
    sql = "select * from definition where location =" + "'" + location + "'"
    cursor2.execute(sql)

    result = cursor2.fetchall()

    line_number_array = []

    for row in result:
        line_number_array.append(int(unicode(row[6])))

    #print line_number_array

    line_number_array_uniq = list(set(line_number_array))
    x = np.sort(line_number_array_uniq).tolist()
     
    y = np.searchsorted(x, int(linenumber), side='right')

    try:    
        caller_ln = str(x[y-1])
        callee_ln = linenumber
    except:
        caller_ln = 0
        pass

    try:
        cursor3 = connector.cursor()
        sql = "select * from definition where location =" + "'" + location + "' AND linenumber =" + "'" + str(x[y-1]) + "'"
        cursor3.execute(sql)
        result = cursor3.fetchall()
    except:
        continue
    
        
    #print result

    counter = 0

    cursor4 = connector.cursor()
    
    for row in result:
        str_definition = unicode(row[4]) + ":" + unicode(row[5]) + ":" + unicode(row[6])

        print str_callchain + " <- " + str_definition

        tmpcaller = str_definition.split(":")
        tmpcallee = str_callchain.split(":")

        print "-- caller " + tmpcaller[0]
        print "-- callee " + tmpcallee[0]
        print "-- location " + location
        print "-- caller_ln " + str(caller_ln)
        print "-- callee_ln " + str(callee_ln)

        sql = "INSERT INTO ex (id, software_version, caller_name, caller_linenumber, callee_name, callee_linenumber, location) VALUES (" + str(counter) + ", '" + software_version + "', '" + tmpcaller[0] + "', '" + str(caller_ln) + "', '" +tmpcallee[0] + "', '" + str(callee_ln) + "', '" + str(location) +"');"

        print sql

        cursor4.execute(sql)
        connector.commit()

        counter = counter + 1

cursor.close()
connector.close()

