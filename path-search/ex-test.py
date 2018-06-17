# python ex-list.py bind999b1 isc_buffer_allocate

import time
import psycopg2
import os

import sys
import re
import commands

argvs = sys.argv  
argc = len(argvs) 

dbname = argvs[1]
funcname = argvs[2]

connection = psycopg2.connect(host="192.168.1.1", port=5432, database=dbname, user="postgres", password="")

cursor = connection.cursor()
sqlstr = "SELECT * FROM ex where callee_name=\'" + funcname + "\'" + ";"
cursor.execute(sqlstr)
stats = cursor.fetchall()

print stats
