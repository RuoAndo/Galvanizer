# usage: python ex.py

from pymongo import MongoClient

connect = MongoClient("127.0.0.1", 27017)
l = connect.database_names()

print l
