# python 1.py tools/libxl/libxl.c libxl 372

import sys 
import commands
import os

argvs = sys.argv  
argc = len(argvs) 

f = open(argvs[1])

line = f.readline() 

while line:
    tmp = line.split(",")
    #print tmp

    #python search.py xen_test xen/common/sched_credit2.c 310

    comstr = "python search3.py " + argvs[2] + " " + tmp[2].strip() + " " + tmp[1]
    #print comstr 
    check = commands.getoutput(comstr)
    print tmp[0] + "," + tmp[1] + "," + check
    
    line = f.readline()



