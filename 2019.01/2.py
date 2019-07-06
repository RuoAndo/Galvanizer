import sys
import re

argvs = sys.argv  
argc = len(argvs) 

f = open(argvs[1])

line = f.readline() 

while line:
    try:
        line = f.readline()
        tmp = re.split(r'[\s\t+]', line)
        tmp = filter(lambda str:str != '', tmp)
        print tmp[0] + "," + tmp[1] + "," + tmp[2]
    except:
        pass
f.close

