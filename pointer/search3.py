from pymongo import MongoClient

import numpy
import numpy as np
import sys

argvs = sys.argv  
argc = len(argvs) 

software_version = argvs[1]
loc = argvs[2]
ln = argvs[3]

connect = MongoClient("127.0.0.1", 27017)
db= connect[software_version]
collect = db['definition']

line_number_array = []

ret = collect.find({"location" : loc})

for doc in ret:
    #print doc
    if doc['linenumber'].isdigit() == True:
        line_number_array.append(int(doc['linenumber']))

line_number_array_uniq = list(set(line_number_array))
x = np.sort(line_number_array_uniq).tolist()

#print x

y = np.searchsorted(x, int(ln), side='left')
#print "x:" + str(x)
#print "ln:" +  str(ln)
#print "y:" + str(y)
#print "len(x):" + str(len(x))
#print "x(y):" + str(x[y])

lns = x[y-1]

caller_array = []
ret2 = collect.find({"linenumber" : str(lns), "location" : loc})
for doc2 in ret2:
    #print doc2
    caller_array.append(doc2['function_name'])
    caller_array_uniq = list(set(caller_array))
                
#print caller_array_uniq[0]
#print loc + ":" + str(ln) + ":" + str(caller_array_uniq[0]) + ":" + loc + ":" + str(lns)

#print str(caller_array_uniq[0]) + "," + loc + "," + str(lns)

db2= connect[software_version]
collect2 = db2['ex']

ret2 = collect2.find({"callee" : str(caller_array_uniq[0])})
callee_count = ret2.count()
#for doc2 in ret2:
#    print doc2.count()

ret2 = collect2.find({"caller" : str(caller_array_uniq[0])})
caller_count = ret2.count()
      
print str(caller_array_uniq[0]) + "," + loc + "," + str(lns) + "," + str(caller_count) + "," + str(callee_count) 
