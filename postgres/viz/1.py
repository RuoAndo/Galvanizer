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

while line:

    line2 = line.strip("*").replace("*","")
    tmp = line2.split(",")

    try:
        ret = collect.find({"src" : tmp[2]})
        
        for doc in ret:
            #print doc
            if len(doc["dst"]) != 0:
                print doc["src"] + "[color=blue penwidth=3];"
    except:
        pass
                
    if len(tmp) == 7:
        #tmp2 = tmp[6].split("/")
        #print tmp[4].strip("{").strip("}") + "__" + tmp2[-1].replace(".","_").replace("-","_").rstrip() + "->" + tmp[2].strip("{").strip("}")
        print tmp[4].strip("{").strip("}") + "->" + tmp[2].strip("{").strip("}")
    else:
        try:
            print tmp[1].strip("{") + "->" + tmp[0].strip("{").strip("}")
        except:
            pass
            
    line = f.readline() 

print "}"
