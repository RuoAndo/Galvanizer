#!/usr/bin/env python
# -*- coding:utf-8 -*-

import csv
import sys 

import sys
#from pymongo import Connection
from pymongo import MongoClient

import numpy
import numpy as np

argvs = sys.argv 

insert_ip = str(argvs[4])

#connection
#connect = Connection('localhost', 27017)
connect = MongoClient(insert_ip, 27017)

#testdbを取得
#db = connect.test
#次のような記述もOK db = con['test']
db = connect[str(argvs[2])]

#db名を出力
print "db name is = "
print db.name

#foo collection
#collect = db.gtags_rx
collect_string = str(argvs[3])
#次のような記述もOK 
collect = db[collect_string]
 
f = open(argvs[1], 'rt')

reader = csv.reader(f)
header = next(reader)

for row in reader:
    print row
    # col.insert({'user':'symfo', 'values':{'key1':'v1'}, 'tags' : ['dog', 'cat'], 'number' : 1})
    collect.insert({'function_name':row[0], 'line_number':int(row[1]), 'file_name':row[2]})

    #collect1.save({row[0]:int(row[1])})
    #collect2.save({row[0]:row[2]})

f.close()
