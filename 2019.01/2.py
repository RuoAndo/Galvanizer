import sys
import re

argvs = sys.argv  
argc = len(argvs) 

f = open(argvs[1])

line = f.readline() 

while line:
    line = f.readline()
    #tmp = line.split("\t")
    tmp = re.split(r'[\s\t+]', line)
    #line = re.sub(r"[ +]", "\,", line)
    #tmp.remove("").strip()
    tmp = filter(lambda str:str != '', tmp)
    #print tmp
    print tmp[0] + "," + tmp[1] + "," + tmp[2]
f.close

