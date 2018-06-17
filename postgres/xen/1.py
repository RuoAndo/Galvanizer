# python 1.py tools/libxl/libxl.c libxl 372

import sys 
import commands
import os

argvs = sys.argv  
argc = len(argvs) 

f = open(argvs[1])

line = f.readline() 

while line:
    
    tmp =  line.split("/")
    if len(tmp) == 6:
        #print line
        #print tmp[5].rstrip()

        tmp2 = tmp[5].split("-")
        tmp3 = tmp2[1].split("tar")

        #print tmp3[0].rstrip(".")
        #wget http://bits.xensource.com/oss-xen/release/4.1.0/xen-4.1.0.tar.gz
        #print wgetstr
        
        wgetstr = "wget http://bits.xensource.com/oss-xen/release/" + tmp3[0].rstrip(".") + "/" + tmp[5].rstrip()

        os.system(wgetstr)
        #check = commands.getoutput(wgetstr)
        #print check
        
    line = f.readline()



