# python realloc.py libxl.c

from pymongo import MongoClient

import sys 
import re

connect = MongoClient("127.0.0.1", 27017)                                                                           
db= connect['sat']                                                 
#db.drop_collection(db.relloc)
#db.drop_collection(db.looptype)
collect = db['realloc']

#pattern = r"for.*\(.*\;.*\;"
#pattern2 = r"[a-zA-Z0-9_]"

argvs = sys.argv  
argc = len(argvs) 

f = open(argvs[1])

line = f.readline() 

print "processing " + argvs[1] + "..." 
linenumber = 1
while line:
    if line.find("realloc") > -1:
        print line.strip() + ":" + str(linenumber)

        tmp = line.split("realloc")
        #print tmp
        tmp3 = tmp[0].split("=")
        lhs = tmp3[0].lstrip().rstrip()
        print lhs

        tmp2 = tmp[1].split(",")

        collect.insert( { 'type' : "realloc-line", 'linenumber' : linenumber, 'lhs' : lhs, 'location' : argvs[1], 'line' : line.strip() } )
            
        for num in range(0, len(tmp2)):
            argstr = tmp2[num].replace(';', '')
            print argstr

            collect.insert( { 'type' : "realloc", 'linenumber' : linenumber, 'argument' : argstr, 'lhs' : lhs, 'location' : argvs[1], 'line' : line.strip()} )



    line = f.readline()
    linenumber = linenumber + 1
