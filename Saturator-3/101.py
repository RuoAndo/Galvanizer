# saturator-2 : callchain extractor using gtags. 
# this program uses gtags (global) and mongoDB

# mongoDB [callchain list (gtags -rx)] -- find() -->  saturator-2 [ function list (gtags -f) ]

# mongoDB <-- insert() --  saturator-2
# collect_caller.insert( { 'caller_name' : doc3['function_name'], 'caller_line_number' : line_number_array[x-1], 'ID_name' : str(row[0]), 'ID_line_number' : int(tmp), 'file_name' : str(row[2]) } )

# ./listup.pl > list
# ./global-t.sh list > flist
# ./3.pl flist > flist2
# ./drem.pl flist2 > flist2-drem
# ./global-rx.sh flist2-drem > flist3
# ./flist_to_csv.pl flist2-drem > flist.csv
# ./flist_to_csv.pl flist3 > list-callchain.csv
# python store_gtags_f_flist.py flist
# python 101.py list-callchain.csv

# requirements:
# mongoDB 
# pymongo (2.7 or later)
# nympy
# global (gtags)

# output sample - python 101.py list-callchain.csv
# { "_id" : ObjectId("561a71d5141a9215e54eafeb"), "caller_line_number" : 352, "file_name" : "tools_ioemu-qemu-xen_linux-user_signal__c", "ID_line_number" : 360, "ID_name" : "_exit", "caller_name" : "force_sig" }

import csv
import sys 

#from pymongo import Connection
from pymongo import MongoClient

import numpy
import numpy as np

# write (insert)
connect2 = MongoClient('192.168.11.4', 27017)
db_2 = connect2.test
collect_caller = db_2.caller

# read (find)
connect3 = MongoClient('192.168.11.3', 27017)
db_3 = connect3.test
collect_f = db_3.gtags_f

argvs = sys.argv 

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
            	collect_caller.insert( { 'caller_name' : doc3['function_name'], 'caller_line_number' : line_number_array[x-1], 'ID_name' : str(row[0]), 'ID_line_number' : int(tmp), 'file_name' : str(row[2]) } )

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
