# python for.py libxl.c

from pymongo import MongoClient

import sys 
import re

connect = MongoClient("127.0.0.1", 27017)                                                                           
db= connect['sat']                                                                                                   
#db.drop_collection(db.forloop)
collect = db['forloop']

pattern = r"for.*\(.*\;.*\;"
pattern2 = r"[a-zA-Z0-9_]"

argvs = sys.argv  
argc = len(argvs) 

f = open(argvs[1])

line = f.readline() 

linecounter = 1
BRACE_depth = 0
for_flag = 0
for_start_linenumber = 0
for_end_linenmber = 0
for_linebackup = ""

print "processing " + argvs[1] + "...."

while line:
    #print line
    matchOB = re.search(pattern , line)
    if matchOB and line.find("for_") == -1 and line.find("_for") == -1:
        print "------"
        print "for detected - flag is up. : " + str(linecounter) + " @ " + str(argvs[1])
        for_start_linenumber = linecounter
        for_linebackup = line
        print line.rstrip()
        for_flag = 1
        
        if line.find("{") > -1:
            BRACE_depth = 1
            print "LB detected:" + str(linecounter)
            #for_start_linenumber = linecounter
        else:
            
            for_linebackup = line

            line = f.readline()
            linecounter = linecounter + 1            

            if line.find("}") == -1 and line.find("if") > 1:
                
                #for_start_linenumber = linecounter
                for_end_linenumber = linecounter

                print "   info:"
                print "   " + for_linebackup.rstrip()
                print "   " + str(for_start_linenumber)
                print "   " + str(for_end_linenumber)                
                
                collect.insert( { 'type' : "forloop", 'linecounter' : linecounter, 'line' : for_linebackup.rstrip(), 'start' : for_start_linenumber, 'end' : for_end_linenumber, 'location' : argvs[1] }) 

            matchOB2 = re.search(pattern2 , line)            
            if matchOB2:
                
                #for_start_linenumber = linecounter
                for_end_linenumber = linecounter
                #for_linebackup = line

                print "   info:"
                print "   " + for_linebackup.rstrip()
                print "   " + str(for_start_linenumber)
                print "   " + str(for_end_linenumber)                

                collect.insert( { 'type' : "forloop", 'linecounter' : linecounter, 'line' : for_linebackup.rstrip(), 'start' : for_start_linenumber, 'end' : for_end_linenumber, 'location' : argvs[1] }) 

    if for_flag == 1 and line.find("{") > -1:
        print str(BRACE_depth) + ":" + str(linecounter)
        BRACE_depth = BRACE_depth + 1

    if for_flag == 1 and line.find("}") > -1:
        print str(BRACE_depth) + ":" + str(linecounter)
        BRACE_depth = BRACE_depth - 1
                    
        if BRACE_depth == 1:
            for_end_linenumber = linecounter
            print "RB detected:" + str(linecounter)
            print "   info:"
            print "   " + for_linebackup.rstrip()
            print "   " + str(for_start_linenumber)
            print "   " + str(for_end_linenumber)

#argvs[1])

            collect.insert( { 'type' : "forloop", 'linecounter' : linecounter, 'line' : for_linebackup.rstrip(), 'start' : for_start_linenumber, 'end' : for_end_linenumber, 'location' : argvs[1]}) 
            
            for_flag = for_flag -1;
            
    linecounter = linecounter + 1
    line = f.readline()
    
