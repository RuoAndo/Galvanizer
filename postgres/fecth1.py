# -*- coding: utf-8 -*- 

# id
# function_name
# location
# linenumber

import psycopg2

connector = psycopg2.connect(host="localhost", database="sample", user="postgres", password="")
cursor = connector.cursor()
cursor.execute("select * from test")

result = cursor.fetchall()

for row in result:
    print "---"
    print "id -- " + unicode(row[0])
    print "function name -- " + unicode(row[1])
    print "location -- " + unicode(row[2])
    print "linenumber -- " + unicode(row[3])

cursor.close()
connector.close()

