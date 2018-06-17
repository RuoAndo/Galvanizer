import sys 
 
argvs = sys.argv  
argc = len(argvs) 

#if (argc < 3):   
#    print 'Usage: # python %s filename' % argvs[0]
#    quit()        
 
f = open(argvs[1])

line = f.readline() 

while line:
    tmp = line.split(":")
    print tmp

    line = f.readline()

f.close

