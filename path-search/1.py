# python 1.py tools/libxl/libxl.c libxl 372

import sys 

from pymongo import Connection
connect = Connection('127.0.0.1', 27017)

db = connect.satpg
collect = db.satpg

argvs = sys.argv  
argc = len(argvs) 

f = open(argvs[1])

line = f.readline() 

print "digraph sample {"

print "START[color=red penwidth=5];"
print "EMPTY[shape=box color=red penwidth=5];"
print "MAIN[shape=box color=red penwidth=5];"
#print "INT[shape=box color=red penwidth=5];"

while line:

    line2 = line.strip("*").replace("*","")
    tmp = line2.split(",")

    if line2.find("START") > -1:
        print "START" + "->" + tmp[0]
        print tmp[0] + "[shape=box color=green penwidth=5];"

    if line2.find("main_")> -1:
        try:
            #print "MAIN" + "->" + tmp[0]
            print tmp[0] + "[shape=box color=blue penwidth=5];"
        except:
            pass
            
    if line2.find("EMPTY") == -1:
        try:
            print tmp[0] + "->" + tmp[2]
        except:
            pass

    else:
        try:
            print tmp[0] + "->" + tmp[1]
        except:
            pass
            
    line = f.readline() 

print "}"
