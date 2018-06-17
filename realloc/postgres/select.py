import time
import psycopg2
import os

import sys
import re
import commands

argvs = sys.argv 

from pymongo import Connection
connect = Connection('127.0.0.1', 27017)

db = connect.pgstat
collect = db.pgstat

connection3 = psycopg2.connect(host="192.168.1.1", port=5432, database="realloc_2", user="postgres", password="")
cursor5 = connection3.cursor()

sqlstr = "SELECT * FROM " + argvs[1]
cursor5.execute(sqlstr)

stats = cursor5.fetchall()

result = {}
for stat in stats:
    print stat[1]

    
