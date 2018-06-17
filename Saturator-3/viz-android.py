# python find4.py 192.168.11.9 saturator3 home_flare_Downloads_xen_4_1_0.callers libxl_list_cpupool 2

import csv
import sys 

from pymongo import Connection
#from pymongo import MongoClient

#import numpy
#import numpy as np

print "digraph {"
#print "layout = circo"
print "node[fontsize=10 shape=box]"

argvs = sys.argv 

target_ip = str(argvs[1])
dbname = str(argvs[2])
collectionname = str(argvs[3]) + ".callers"
functionname = str(argvs[4])
find_depth = int(argvs[5])

print functionname + "[color=red penwidth=5]"

connect = Connection(target_ip, 27017)
db = connect[dbname]
collect_f = db[collectionname]

#{ "_id" : ObjectId("56aa75920dd43c1156551603"), "caller_line_number" : "25", "function_line_number" : "1", "file_name" : "stubdom_grub_osdep__h", "caller_name" : "P", "function_name" : "__OSDEP_H__" }
#{ "_id" : ObjectId("56aa75920dd43c1156551604"), "caller_line_number" : "13", "function_line_number" : "15", "file_name" : "stubdom_grub_osdep__h", "caller_name" : "ntohl", "function_name" : "swap16" }

callers_global = []
callers_global.append("head")

def find(function_name):

    #print callers_global
    #print "query:" + idname

    found_flag = 0
    for x in callers_global:
        if str(x) == function_name:
            found_flag = 1

    if found_flag ==0:
    
        doc = []
        ret = []
        callers = []
        callers_uniq = []

        ret = collect_f.find({ 'function_name' : function_name}).limit(find_depth)

        #print doc

        for doc in ret:
            callers.append(doc['caller_name'])
            #print "mongo_search_array:" + str(doc)

        callers_uniq = list(set(callers))

        for (i,word) in enumerate(callers_uniq):
            if function_name == callers_uniq[i]:
                pass
            else:
                print function_name + "->" + callers_uniq[i]                    
                callers_global.append(function_name)
                find(callers_uniq[i])
                
find(functionname)

print "}"
