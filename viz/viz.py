# usage: python ex.py

from pymongo import MongoClient

import numpy
import numpy as np
import sys

argvs = sys.argv  
argc = len(argvs) 

func = argvs[1]

#{ "_id" : ObjectId("57bac3b1b3051f6c18fdba09"), "caller_ln" : 91, "caller" : "__attribute__", "location" : "tools/vnet/vnet-module/if_varp.h", "callee_ln" : 94, "callee" : "vmac" }

#{ "_id" : ObjectId("57bb0effb3051f6c18001ed6"), "caller_ln" : 3148, "caller" : "libxl_cpupool_cpuremove_node", "location" : "tools/libxl/libxl.c", "callee_ln" : 3157, "callee" : "libxl_list_cpupool" }

connect = MongoClient("127.0.0.1", 27017)
db= connect['sat']
collect = db['ex']

caller_name_array = []

print "digraph sample {"

ret = collect.find({"callee":func}).batch_size(30)

for doc in ret:
    print func + " -> " + doc["caller"]
    caller_name_array.append(doc["caller"])

for i in caller_name_array:
    ret2 = collect.find({"callee":i}).limit(3)
    for doc2 in ret2:
        print i + " -> " + doc2["caller"]

print "}"

