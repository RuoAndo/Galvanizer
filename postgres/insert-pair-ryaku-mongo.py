import sys
import re
import commands

argvs = sys.argv
argc = len(argvs)

from pymongo import MongoClient

connect = MongoClient("127.0.0.1", 27017)
db= connect['pg_dbpairname']
collect = db['pg_dbpairname']

ret = collect.find()

#collect.insert({'_id' : argvs[1], 'name' : argvs[2], 'ryaku' : argvs[3]})
collect.insert({'_id' : argvs[1], 'name' : argvs[2]})


