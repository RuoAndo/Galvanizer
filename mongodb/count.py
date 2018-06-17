import sys 
from pymongo import MongoClient

argvs = sys.argv  
argc = len(argvs) 

software_version = argvs[1]

array = []
counter = 0

connect = MongoClient('127.0.0.1', 27017)
db = connect[software_version]
collect = db.definition
collect2 = db.callee
collect3 = db.ex

N1 = collect.count()
N2 = collect2.count()
N3 = collect3.count()
print str(N1) + ":" + str(N2) + ":" + str(N3)
