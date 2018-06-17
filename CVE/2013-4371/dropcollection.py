from pymongo import MongoClient

import sys 
import re

connect = MongoClient("127.0.0.1", 27017)                                                                           
db= connect['sat']                                                 
db.drop_collection(db.relloc)
db.drop_collection(db.looptype)
db.drop_collection(db.forloop)
db.drop_collection(db.cve-2013-4371)
