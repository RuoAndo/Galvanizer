# python find4.py 192.168.11.9 saturator3 home_flare_Downloads_xen_4_1_0.callers libxl_list_cpupool 2

import csv
import sys 

#from pymongo import Connection
from pymongo import MongoClient

#import numpy
#import numpy as np

#print "digraph {"
#print "layout = circo"
print "node[fontsize=10 shape=box]"

argvs = sys.argv 

target_ip = str(argvs[1])
dbname = str(argvs[2])
collectionname = str(argvs[3])
functionname = str(argvs[4])
find_depth = int(argvs[5])

print functionname + "[color=red penwidth=5]"

connect = MongoClient(target_ip, 27017)
db = connect[dbname]
collect_f = db[collectionname]

#> db.home_flare_Downloads_xen_4_1_0.callers.find({"ID_name" : "libxl_list_cpupool"})
#{ "_id" : ObjectId("567e130e0dd43c3e1412518f"), "caller_line_number" : 3134, "file_name" : "tools_libxl_libxl__c", "ID_line_number" : 3152, "ID_name" : "libxl_list_cpupool", "caller_name" : "xc_cpupool_removecpu" }
#{ "_id" : ObjectId("567e130f0dd43c3e14125190"), "caller_line_number" : 404, "file_name" : "tools_libxl_libxl__h", "ID_line_number" : 418, "ID_name" : "libxl_list_cpupool", "caller_name" : "libxl_vncviewer_exec" }
#{ "_id" : ObjectId("567e130f0dd43c3e14125191"), "caller_line_number" : 42, "file_name" : "tools_libxl_libxl_utils__c", "ID_line_number" : 147, "ID_name" : "libxl_list_cpupool", "caller_name" : "XEN_SCHEDULER_CREDIT2" }
#{ "_id" : ObjectId("567e13100dd43c3e14125192"), "caller_line_number" : 5488, "file_name" : "tools_libxl_xl_cmdimpl__c", "ID_line_number" : 5493, "ID_name" : "libxl_list_cpupool", "caller_name" : "stderr" }
#{ "_id" : ObjectId("567e13110dd43c3e14125193"), "caller_line_number" : 5789, "file_name" : "tools_libxl_xl_cmdimpl__c", "ID_line_number" : 5813, "ID_name" : "libxl_list_cpupool", "caller_name" : "n" }

callers_global = []
callers_global.append("head")

def find(idname):

    #print callers_global
    #print "query:" + idname

    found_flag = 0
    for x in callers_global:
        if str(x) == idname:
            found_flag = 1

    if found_flag ==0:
    
        doc = []
        ret = []
        callers = []
        callers_uniq = []

        ret = collect_f.find({ 'caller_name' : idname}).limit(find_depth)

        for doc in ret:
            callers.append(doc['function_name'])
            #print "mongo_search_array:" + str(doc)

        callers_uniq = list(set(callers))

        for (i,word) in enumerate(callers_uniq):
            if idname == callers_uniq[i]:
                pass
            else:
                #print idname + "->" + callers_uniq[i]  

                print idname + "->" + callers_uniq[i]+ "[color=\"red\"]"                    
                #print callers_uniq[i] + "->" + idname + "[color=\"red\"]"                    
                callers_global.append(idname)
                find(callers_uniq[i])
                
find(functionname)

#print "}"
