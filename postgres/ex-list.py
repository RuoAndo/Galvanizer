
# python ex-list.py bind999b1 isc_buffer_allocate

import time
import psycopg2
import os

import sys
import re
import commands

argvs = sys.argv  
argc = len(argvs) 

from pymongo import Connection
connect = Connection('127.0.0.1', 27017)

# mongoDB: pgstat.pgstat

db = connect.satpg
collect = db.satpg
collect2 = db.nodes
db.satpg.drop()
db.nodes.drop()

dbname = argvs[1]
funcname = argvs[2]

print funcname + "," + "START"

def traverse(funcname):
    #print funcname
    
    connection = psycopg2.connect(host="192.168.1.1", port=5432, database=dbname, user="postgres", password="")

    cursor = connection.cursor()
    sqlstr = "SELECT * FROM ex where callee_name=\'" + funcname + "\' LIMIT " + argvs[3] + ";"
    cursor.execute(sqlstr)
    stats = cursor.fetchall()

    #print stats
    if len(stats) == 0:
        print "EMPTY" + "," + funcname 
        exit

    counter = 0
    for stat in stats:
        #print stat
        #print stat[2] + "->" + stat[4] + ":" + stat[6]
        print str(stat[0]) + "," + stat[1] + "," + stat[2].strip("{").strip("}") + "," + str(stat[3]) + "," + stat[4].strip("{").strip("}") + "," + str(stat[5]) + "," + stat[6]

        ret = collect.find({"src":stat[2]})

        flag = 0
        for doc in ret:
            #print doc
            if doc["dst"] == stat[4]:
                flag = 1

        if flag == 0:
            collect.insert({"src":stat[2], "dst":stat[4]})
            #collect2.insert({"_id": stat[2]})
            #collect2.insert({"_id": stat[4]})
            
            #if stat[2] == stat[4]:
            #    break
        
            if counter < 5:
                traverse(stat[2])
        
        counter = counter + 1

    cursor.close
    connection.close
        
if __name__ == "__main__":
    traverse(funcname)
