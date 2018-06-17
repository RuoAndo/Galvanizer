# usage: python viz1.py bind_9_9_9_P3 isc_buffer_allocate

# -bash-4.1# python viz1.py bind_9_9_9_P3 isc_buffer_allocate > tmp                                                                        
# -bash-4.1# dot -o tmp.png -Tpng tmp                                                                              
# -bash-4.1# cp tmp.png /var/www/html/codes/       

from pymongo import MongoClient
import sys

argvs = sys.argv  

import numpy
import numpy as np

connect = MongoClient("127.0.0.1", 27017)

dbname = argvs[1]
funcname = argvs[2]

db = connect[dbname]

collect = db['ex']

func_name_array = []
#ret = collect.find({"callee":funcname}).batch_size(30).limit(10)
ret = collect.find({"callee":funcname}).batch_size(30).limit(10)

print "digraph sample {"

caller_name_array = []

for doc in ret:                                                                                                                            
    print funcname + " -> " + doc["caller"]                                                                                                
    caller_name_array.append(doc["caller"])                                                                                                

for i in caller_name_array:                                                                                                                
    ret2 = collect.find({"callee":i}).limit(3)                                                                                             
    for doc2 in ret2:                                                                                                                      
        print i.strip("{").strip("}") + " -> " + doc2["caller"].strip("{").strip("}")

print "}"
