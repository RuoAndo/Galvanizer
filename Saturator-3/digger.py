import csv
import sys 

#from pymongo import Connection
from pymongo import MongoClient

import numpy
import numpy as np

argvs = sys.argv 

target_ip = str(argvs[1])
dbname = str(argvs[2])
collectionname = str(argvs[3])
functionname = str(argvs[4])
linenumber = str(argvs[5])

connect = MongoClient(target_ip, 27017)
db = connect[dbname]
collect_f = db[collectionname]

# python digger.py 192.168.11.4 saturator3 home_flare_linux_3_0_1_arch cpm_smc 72
#ret = collect_f.find()
ret = collect_f.find({ 'function_name' : functionname, 'line_number' : int(linenumber) })

line_number_array = []

for doc in ret:
    file_name = doc['file_name']
    line_number = doc['line_number']

    ret2 = collect_f.find({ 'file_name' : file_name })
    for doc2 in ret2:
        #print doc2
        line_number_array.append(doc2['line_number'])
        
    print line_number_array

    x = np.searchsorted(line_number_array, line_number, side='left')

    #print file_name + ":" + str(line_number) + "->" + file_name + ":" + str(line_number_array[x-1]) 

    ret3 = collect_f.find({ 'file_name' : file_name, 'line_number' : line_number_array[x-1]})

    for doc3 in ret3:
        print doc3['file_name'] + ":" + doc3['function_name'] + ":" + str(doc3['line_number']) + "->" + file_name + ":" + functionname + ":" + str(line_number)
