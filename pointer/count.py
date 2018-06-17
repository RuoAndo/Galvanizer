import sys 
import commands
import os

argvs = sys.argv  
argc = len(argvs) 

f = open(argvs[1])

line = f.readline() 

while line:
    comstr = "grep alloc " + line.rstrip() + " | wc -l"
    alloc_ = commands.getoutput(comstr)

    comstr = "grep for " + line.rstrip() + " | wc -l"
    for_ = commands.getoutput(comstr)

    comstr = "grep if " + line.rstrip() + " | wc -l"
    if_ = commands.getoutput(comstr)

    comstr = "grep free " + line.rstrip() + " | wc -l"
    free_ = commands.getoutput(comstr)

    all = alloc_ + "," + for_ + "," + if_ + "," + free_
    
    print line.rstrip() + "," + all
    line = f.readline()
    



