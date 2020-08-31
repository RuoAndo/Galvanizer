import sys
import re

argvs = sys.argv  
argc = len(argvs) 

f = open(argvs[1])

line = f.readline() 

while line:
    try:    
        line = f.readline()
        #tmp = re.split(r'[\s+]', line)
        tmp = re.split(r':', line)
        print("b " + tmp[0] + ":" + tmp[1])
    except:
        pass
f.close

