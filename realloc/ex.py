# usage: python ex.py

from pymongo import MongoClient

import numpy
import numpy as np
import sys

argvs = sys.argv  
argc = len(argvs)

version = argvs[1]
connect = MongoClient("127.0.0.1", 27017)

db= connect[version]
collect = db['definition']

db2= connect['realloc']
collect2 = db2[version]

dbstr = version + "_realloc"
db3= connect['realloc']
collect3 = db3[dbstr]

ret2 = collect2.find()

for doc2 in ret2:
    print doc2['file_name']
    
    ret = collect.find({"location":doc2['file_name']})
    
    line_number_array = []
    for doc in ret:
        line_number_array.append(int(doc['linenumber']))

    #print line_number_array
    line_number_array_uniq = list(set(line_number_array))
    x = np.sort(line_number_array_uniq).tolist()
    print x

    ln = int(doc2['line_number'])
    y = np.searchsorted(x, int(doc2['line_number']), side='left')
    print "x:" + str(x)
    print "ln:" +  str(doc2['line_number'])
    print "y:" + str(y)

    if y != 0 and y < len(x):
        if int == x[y]:
            lns = ln
        else:
            lns = x[y-1]

        print lns

        ret3 = collect.find({"linenumber" : str(lns), "location" : doc2['file_name']}).limit(1)
        for doc3 in ret3:
            print doc3

            try:
                collect3.insert({"function": doc3['function_name'], "realloc_linenumber":doc2['line_number'], "function_linenumber":lns})
            except:
                pass
