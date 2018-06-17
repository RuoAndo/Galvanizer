import sys 
 
from pymongo import MongoClient

argvs = sys.argv  
argc = len(argvs) 

#print argvs
#print argc
#print

if (argc < 3):   
    print 'Usage: # python %s filename' % argvs[0]
    quit()        
 
#print 'The content of %s ...n' % argvs[1]

connect = MongoClient('192.168.11.4', 27017)
db_2 = connect[str(argvs[2])]
collect_caller = db_2.caller

print "edge [penwidth = 5 color=green];"
#echo "edge [penwidth = 5 color=red];" >> tmpdot

f = open(argvs[1])

line = f.readline() 

while line:
    #print line
    line = f.readline()
    
    if line.find('_id') > -1:    
        tmp = line.split(',')
        #print tmp[5]
        tmp2 = tmp[5].split(':')
        
        str(tmp2[1]).replace('\"', '')
        s1 = tmp2[1].replace(' ', '')
        s2 = s1.replace('}', '')
        s3 = s2.replace('\n', '')
        s4 = s3.replace('\"', '')

        #print s4

        ret = collect_caller.find({ 'ID_name' : s4 })

        for doc in ret:
            #print doc
            
            doc_tmp = str(doc).split(',')
            #print doc_tmp[2]
            
            doc_tmp2 = doc_tmp[2].split(':')
            #print doc_tmp2[1]

            s5 = doc_tmp2[1].replace('u', '')
            s6 = s5.replace('\'', '')
            s7 = s6.replace(' ', '')

            if s7 == "main":
                print "edge [penwidth = 5 color=red];"
                print s4 + " ->" + s7

            else:
                print "edge [penwidth = 5 color=green];"
                print s4 + " ->" + s7


            # str(tmp2[1]).replace('\"', '')
            

f.close

