# -*- coding: utf-8 -*- 

import psycopg2

connector = psycopg2.connect(host="127.0.0.1", database="sample", user="postgres", password="")
cursor = connector.cursor()
cursor.execute("select * from callchain")

result = cursor.fetchmany(1)

#1 id : 1 
#2 software_version : bind998
#3 listtype : callchain
#4 function_name : libxl_string_list_destroy(libxl_string_list *psl)
#5 location : drivers/hwmon/smsc47m1.c
#6 linenumber : 240

for row in result:
    print "---"
    print "id -- " + unicode(row[0])
    print "software_version -- " + unicode(row[1])
    print "listtype -- " + unicode(row[2])
    print "function_name -- " + unicode(row[3])

    location = unicode(row[4])
    print "location -- " + unicode(row[4])
    print "linenumber -- " + unicode(row[5])

cursor2 = connector.cursor()
sql = "select * from definition where location =" + "'" + location + "'"
cursor2.execute(sql)

#result = cursor2.fetchmany(3)
result = cursor2.fetchall()

#print result

line_number_array = []

#1 id : 1 
#2 software_version : bind998
#3 linktype : definition
#4 function_type : void, int ..
#5 function_name : libxl_string_list_destroy(libxl_string_list *psl)
#6 location : lib/dns/diff.c
#7 linenumber : 443

for row in result:
    print "---"
    print "id -- " + unicode(row[0])
    print "software_version -- " + unicode(row[1])
    print "listtype -- " + unicode(row[2])
    print "function_type -- " + unicode(row[3])
    print "function_name -- " + unicode(row[4])
    print "location -- " + unicode(row[5])
    print "linenumber -- " + unicode(row[6])

    line_number_array.append(unicode(row[6]))

print line_number_array

cursor.close()
connector.close()

