import sys
import re

argvs = sys.argv  
argc = len(argvs) 

f = open(argvs[1])

line = f.readline() 

while line:
    line = f.readline()
    #tmp = line.split("\t")
    tmp = re.split(r'[\s+]', line)
    print tmp[0]
f.close

