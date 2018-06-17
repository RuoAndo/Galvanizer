# -*- coding: utf-8 -*- 

# fetch-definition.py

#1 id : 1 
#2 software_version : bind998
#3 listtype : callchain
#4 function_name : libxl_string_list_destroy(libxl_string_list *psl)
#5 location : drivers/hwmon/smsc47m1.c
#6 linenumber : 240

import psycopg2

connector = psycopg2.connect(host="localhost", database="sample", user="postgres", password="")
cursor = connector.cursor()
cursor.execute("select * from callchain")

result = cursor.fetchall()

for row in result:
    print "---"
    print "id -- " + unicode(row[0])
    print "software_version -- " + unicode(row[1])
    print "listtype -- " + unicode(row[2])
    print "function_name -- " + unicode(row[3])
    print "location -- " + unicode(row[4])
    print "linenumber -- " + unicode(row[5])

cursor.close()
connector.close()

