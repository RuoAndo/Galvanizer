import sys 

from pymongo import MongoClient

argvs = sys.argv

target_ip = str(argvs[1])
dbname = str(argvs[2])

connect = MongoClient(target_ip, 27017)
connect.drop_database(dbname)       
