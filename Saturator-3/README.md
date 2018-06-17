<pre>
# saturator-3 : callchain extractor using gtags. 
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

# using mongoDB:
# 
# mongo 1 [192.168.11.3] (gtags -f) ----> find() ---> saturator(numpy) 
# ---> insert() ----> mongo2 (output sample) [192.168.11.4] 

# 
# you could use mongoDB in localhost also.

# write (insert)
# connect = MongoClient('192.168.11.4', 27017)
#db_2 = connect2.
#db_2 = connect[str(argvs[2])]
#collect_caller = db_2.caller

# read (find)
#connect2 = MongoClient('192.168.11.3', 27017)
#db_3 = connect3.test
#db_3 = connect2[str(argvs[2])]
#collect_f = db_3.gtags_f

visualize memo 2016-02-02

./find4.sh x411_func_dump_drem 

visualize memo 2016-02-02

ls | grep apk > list
./do-auto-android-viz.sh list

</pre>