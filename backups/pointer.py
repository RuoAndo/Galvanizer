# python pointer.py libxl.c

from pymongo import MongoClient

import sys 
import re

connect = MongoClient("127.0.0.1", 27017)                                                                           
db= connect['sat']                                                 
collect = db['pointer']

#pattern = r"[a-zA-Z]\s\*[a-zA-Z]\;"
#pattern = r"[a-zA-Z]"
#pattern = r"for.*\(.*\;.*\;"
#pattern2 = r"[a-zA-Z0-9_]"

argvs = sys.argv  
argc = len(argvs) 

f = open(argvs[1])

line = f.readline() 

linenumber = 1
while line:
    #matchOB = re.search(pattern , line)
    #if matchOB > -1:
    #    print line

    if line.find("*") > -1 and line.find(";") > -1:
        print line.strip() + ":" + str(linenumber)

        collect.insert( { 'type' : "pointer", 'linenumber' : linenumber, 'line' : line} )

    #print line
    line = f.readline() 
    linenumber = linenumber + 1
