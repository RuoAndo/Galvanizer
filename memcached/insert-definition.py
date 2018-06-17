import sys 
import memcache
 
argvs = sys.argv  
argc = len(argvs) 

#if (argc < 3):   
#    print 'Usage: # python %s filename' % argvs[0]
#    quit()        
 
f = open(argvs[1])

line = f.readline() 

#memcachedclient = memcache.Client(['127.0.0.1:11211'])
#memcachedclient.flush_all()

while line:
    tmp = line.split(":")
    print tmp

    # python readline.py sample-definition                                                                           
    # ['va_start', 'va_start#define\tva_start(ap, last) \\', 'acconfig.h', '114\n']
    # ['loadkeys', 'loadkeys(char *dirname, char *setname)', 'bin/dnssec/dnssec-dsfromkey.c', '63\n']

    cachedata = "definition__" + tmp[2] + "__" + tmp[3].rstrip()
    # print "set:" + cachedata
    memcachedclient = memcache.Client(['127.0.0.1:11211'])
    #memcachedclient.flush_all()
    memcachedclient.set(tmp[0], cachedata)

    # print tmp[0]
    #memcachedclient = memcache.Client(['127.0.0.1:11211'])
    cacheddata = memcachedclient.get(tmp[0])
    print cacheddata

    line = f.readline()

f.close

