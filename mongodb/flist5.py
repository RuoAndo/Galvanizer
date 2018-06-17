import sys 
from pymongo import MongoClient

argvs = sys.argv  
argc = len(argvs) 

f = open(argvs[1])
software_version = argvs[2]

array = []
counter = 0

connect = MongoClient('127.0.0.1', 27017)
db = connect[software_version]
collect = db.callee

line = f.readline() 

while line:

    print "-------------"

    print line

    if line.find('(') > -1 and line.find(')') > -1:

        
            #uint64_t vhash(unsigned char m[],vmac_ctx_t *ctx):xen/crypto/vmac.c:846
            #uint64_t vmac(unsigned char m[],vmac_ctx_t *ctx):xen/crypto/vmac.c:951

            print line

            tmp = line.split(":")
            print tmp

            try:
                collect.insert( { 'type' : "callee", 'function_name' :  tmp[0], 'location' : tmp[2],  'linenumber' : tmp[3], 'state' : tmp[1], 'line' : line } )

            except:
                pass

    line = f.readline() 
