# usage: python ex.py

from pymongo import MongoClient

import numpy
import numpy as np
import sys

argvs = sys.argv  
argc = len(argvs) 
software_version = argvs[1]
connect = MongoClient("127.0.0.1", 27017)
db= connect[software_version]
collect = db['definition']
collect2 = db['callee']
collect3 = db['ex']

func_name_array = []
ret = collect2.find().batch_size(30)

for doc in ret:

    if doc['function_name'] != "":

        fn = doc['function_name']
        loc = doc['location']

        try:
            ln = int(doc['linenumber'].strip())
        except:
            continue

        print "--------------"
        print "fn:" + fn + ":loc:" + loc + ":ln:" + str(ln)

        line_number_array = []

        ret2 = collect.find({"location" : loc})
        for doc2 in ret2:
            #print doc2
            if doc2['linenumber'].isdigit() == True:
                line_number_array.append(int(doc2['linenumber']))

        line_number_array_uniq = list(set(line_number_array))


        #print type(line_number_array_uniq)
        x = np.sort(line_number_array_uniq).tolist()
        #print type(x)
        #print x
     
        y = np.searchsorted(x, int(ln), side='left')
        print "x:" + str(x)
        print "ln:" +  str(ln)
        print "y:" + str(y)
        print "len(x):" + str(len(x))

        if y != 0 and y < len(x):
            if ln == x[y]:
                lns = ln
            else:
                lns = x[y-1]

            #print x
            #print ln
            print "lns:" + str(lns)

            caller_array = []
            ret3 = collect.find({"linenumber" : str(lns), "location" : loc})
            for doc3 in ret3:
                caller_array.append(doc3['function_name'])
                caller_array_uniq = list(set(caller_array))
                
            print caller_array_uniq[0]

            collect3.insert({"callee" : fn, "location" : loc, "callee_ln" : ln, "caller" : caller_array_uniq[0], "caller_ln" : lns})
