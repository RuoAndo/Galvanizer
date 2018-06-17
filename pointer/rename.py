import sys 
import commands
import os

argvs = sys.argv  
argc = len(argvs) 

f = open(argvs[1])

line = f.readline() 

while line:
    tmpname = line.lstrip('fn-')
    comstr = "\cp " + line.rstrip() + " " + tmpname.rstrip()
    print comstr
    check = commands.getoutput(comstr)
    line = f.readline()
    



