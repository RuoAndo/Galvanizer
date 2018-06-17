# python find.py 192.168.11.9 saturator3 home_flare_Downloads_xen_4_1_0.callers libxl_list_cpupool

import csv
import sys 

#from pymongo import Connection
from pymongo import MongoClient

#import numpy
#import numpy as np

print "digraph {"
print "layout = circo"
print "node[fontsize=10 shape=box]"

argvs = sys.argv 

target_ip = str(argvs[1])
dbname = str(argvs[2])
collectionname = str(argvs[3])
functionname = str(argvs[4])
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

ret = collect_f.find({ 'ID_name' : functionname})

callers = []

for doc in ret:
    #print doc

    print functionname + "->" + doc['caller_name']

    callers.append(doc['caller_name'])

    #file_name = doc['file_name']
    #line_number = doc['line_number']

#print callers

callers2 = []
callers2_2 = []

for (i,word) in enumerate(callers):
    #print callers[i]

    if str(callers[i]) == "n" or str(callers[i]) == "stderr" or str(callers[i]) == "err" or str(callers[i]) == "or" or str(callers[i]) == "file" or str(callers[i]) == "domid_t":
        pass

    else:

        callers2 = []
        ret2 = collect_f.find({ 'ID_name' : callers[i]})
        for doc2 in ret2:
            #print doc2
            #caller2_str = str(doc2['caller_name']) + "_" + str(doc2['caller_line_number'])
            caller2_str = str(doc2['caller_name'])

            #callers2.append(doc2['caller_name'])
            callers2.append(caller2_str)

            #callers2_uniq = list(set(callers2))

            callers2_uniq = []
            for x in callers2:
                if x not in callers2_uniq:
                    callers2_uniq.append(x)

            #print callers2_uniq

        for (j,word2) in enumerate(callers2_uniq):

            if callers2_uniq[j] != "node":
                print callers[i] + "->" + callers2_uniq[j]

                #if str(callers2_uniq[j]) == "n" or str(callers2_uniq[j]) == "stderr" or str(callers2_uniq[j]) == "err" or str(callers2_uniq[j]) == "op" or str(callers2_uniq[j]) == "file" or str(callers2_uniq[j]) == "domid_t":

                if str(callers2_uniq[j]) == "n" or str(callers2_uniq[j]) == "stderr" or str(callers2_uniq[j]) == "err" or str(callers2_uniq[j]) == "op" or str(callers2_uniq[j]) == "file" or str(callers2_uniq[j]) == "domid_t" or str(callers2_uniq[j]) == "pyxc_error_to_exception":

                    pass

                else:

                    callers3 = []
                    ret3 = collect_f.find({ 'ID_name' : callers2_uniq[j]})
                    for doc3 in ret3:
                        callers3.append(doc3['caller_name'])

                        callers3_uniq = []
                        for x in callers3:
                            if x not in callers3_uniq:
                                callers3_uniq.append(x)

                                #print callers2_uniq

                    for (k,word3) in enumerate(callers3_uniq):
                        print callers2_uniq[j] + "->" + callers3_uniq[k]


print "}"
