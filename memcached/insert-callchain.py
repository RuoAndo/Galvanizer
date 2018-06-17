import sys 
import memcache
 
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

    #va_start:va_start(args, format);:bin/dig/dighost.c:515
    #va_start:va_start(args, format);:bin/dnssec/dnssectool.c:69

    cachedata = "callchain__" + tmp[2] + "__" + tmp[3].rstrip()
    # print "set:" + cachedata
    memcachedclient = memcache.Client(['127.0.0.1:11211'])
    memcachedclient.flush_all()
    memcachedclient.set(tmp[0], cachedata)

    # print tmp[0]
    memcachedclient = memcache.Client(['127.0.0.1:11211'])
    cacheddata = memcachedclient.get(tmp[0])
    print cacheddata

    line = f.readline()

f.close

