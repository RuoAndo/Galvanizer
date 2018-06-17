import csv
import sys 

#from pymongo import Connection
from pymongo import MongoClient

import numpy
import numpy as np

argvs = sys.argv 

insert_ip = str(argvs[5])
find_ip = str(argvs[4])

# write (insert)
connect = MongoClient(insert_ip, 27017)
#db_2 = connect2.
db_2 = connect[str(argvs[2])]

#collect_caller = db_2.caller
collect_caller_string = str(argvs[3]) + ".callers"
collect_caller = db_2[collect_caller_string]

# read (find)
connect2 = MongoClient(find_ip, 27017)
#db_3 = connect3.test
db_3 = connect2[str(argvs[2])]

#collect_f = db_3.gtags_f
collect_f_string = str(argvs[3])
collect_f = db_3[collect_f_string]

f1_rx = open(argvs[1], 'r')
#f2_f = open(argvs[1], 'r')

reader_rx = csv.reader(f1_rx)
#reader_f = csv.reader(f2_f)
#header = next(reader)

#counter = 0

for row in reader_rx:

    print row
    print row[0] + ":" + row[1] + ":" + row[2]
    
    ret = collect_f.find({ 'file_name' : str(row[2]) })
    line_number_array = []

    for doc in ret:
        line_number_array.append(doc['line_number'])
         
    print line_number_array

    try:
        tmp = str(row[1]).strip()
        #print int(tmp)

        x = np.searchsorted(line_number_array, int(tmp), side='left')
        print tmp + ":" + str(line_number_array[x-1]) 

        try:
            ret2 = collect_f.find({ '$and' : [{ 'line_number' : line_number_array[x-1]}, {'file_name' : str(row[2])}] })

            for doc3 in ret2:
                print doc3

	    try: 
            	collect_caller.insert( { 'caller_name' : doc3['function_name'], 'caller_line_number' : line_number_array[x-1], 'function_name' : str(row[0]), 'function_line_number' : int(tmp), 'file_name' : str(row[2]) } )

            	print "----\n"

            except:
               print "error insertion \n"
               continue


        except:
             print "error find() at line_numer \n"
             continue

    except:
        print "skip"

#    if counter == 100:
#        break
        
#    counter = counter + 1


f1_rx.close()
