import csv
import sys 

#from pymongo import Connection
from pymongo import MongoClient

import numpy
import numpy as np

argvs = sys.argv 

target_ip = str(argvs[1])
print "target_ip : " + target_ip

connect = MongoClient(target_ip, 27017)

dbname = str(argvs[2])
print "db_name : " + dbname
db = connect[dbname]

colname = str(argvs[3]) + "_func"
print "col_name : " + colname
collection = db[colname]

colname_loop_caller = colname + "_loop_caller"
collection_loop_caller = db[colname_loop_caller]

loop = collection.find({"property":"forloop"})
#loop = collection.find({"property":"forloop"}).limit(10)

try:
    for doc in loop:
    
        print "loop : " + str(doc['_id'])
        print doc 
    
        print doc['file_name']
        file_name = str(doc['file_name'])

        loop_line_number = doc['line_number']

        if file_name.find('.txt') == -1:

            func = collection.find({"property":"function", "file_name":file_name}).limit(10)

            line_number_array = []
    
            for doc2 in func:
                print doc2
                line_number_array.append(doc2['line_number'])
    
            print line_number_array

            try: 
                x = np.searchsorted(line_number_array, loop_line_number, side='left')
                func_line_number = str(line_number_array[x-1]) 
            
                print "loop line number : " + str(loop_line_number)
                print "sorted (caller) : " + func_line_number

                caller = collection.find({"property":"function", "line_number": int(func_line_number), "file_name":file_name})

                #{u'property': u'forloop', u'_id': ObjectId('5727b38f0dd43c112a735dc4'), u'conditions': u'count = 0; count < nr_pages; count++\n', u'line_number': 148, u'file_name': u'./extras/mini-os/mm.c'}

                #{u'line_number': 94, u'_id': ObjectId('5727b38f0dd43c112a735dc2'), u'file_name': u'./extras/mini-os/mm.c', u'arguments': u'unsigned long first_page, unsigned long nr_pages', u'property': u'function', u'function_name': u'\nstatic void map_free'}

                for doc3 in caller:
                    print doc3
                
                    Nfile_name = doc3['file_name']
                    Nfunction_name = doc3['function_name']
                    Narguments = doc3['arguments']
                
                    Nconditions = doc['conditions']

                    collection_loop_caller.insert( {'file_name' : Nfile_name, 'function_name' : Nfunction_name, 'arguments' : Narguments, 'conditions' : Nconditions })


            except:
                pass

        print "-------"

except: 
    print "error (codec)"
    pass



