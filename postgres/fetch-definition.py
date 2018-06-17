# -*- coding: utf-8 -*- 

# fetch-definition.py

#1 id : 1 
#2 software_version : bind998
#3 linktype : definition
#4 function_type : void, int ..
#5 function_name : libxl_string_list_destroy(libxl_string_list *psl)
#6 location : lib/dns/diff.c
#7 linenumber : 443

import psycopg2

connector = psycopg2.connect(host="localhost", database="sample", user="postgres", password="")
cursor = connector.cursor()
cursor.execute("select * from definition")

result = cursor.fetchall()

for row in result:
    print "---"
    print "id -- " + unicode(row[0])
    print "software_version -- " + unicode(row[1])
    print "linktype -- " + unicode(row[2])
    print "function_type -- " + unicode(row[3])
    print "function_name -- " + unicode(row[4])
    print "location -- " + unicode(row[5])
    print "linenumber -- " + unicode(row[6])

cursor.close()
connector.close()

