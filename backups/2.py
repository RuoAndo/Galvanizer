import sys 
from pymongo import MongoClient

argvs = sys.argv  
argc = len(argvs) 

f = open(argvs[1])

array = []
counter = 0

connect = MongoClient('127.0.0.1', 27017)
db = connect['sat']
collect = db.callee

line = f.readline() 

while line:

    print "-------------"

    print line

    if line.find('(') > -1 and line.find(')') > -1:

        print "TEST:" + line
        try:
            tmp = line.split(":")
            callee = tmp[0]
            print "callee:" + callee
            location = tmp[2]
            print "location:" + location
            linenumber = tmp[3]
            print "linenumber:" + linenumber

            tmp2 = tmp[1].split("(")
            funcname = tmp2[0]

            ##### arguments #####
            
            tmp3 = tmp2[1].split(")")        

            ##### function type and name #####

            tmp4 = funcname.split(" ")
            #print tmp4[-1]

            print str(len(tmp4)) + ":" + str(tmp4) + ":" + tmp4[-1] + ":" + str(tmp3)

            function_type = ""
            for num in range(0, len(tmp4)-1):
                print "   " + tmp4[num]
                function_type = function_type + " " + str(tmp4[num])

                

            print "function_type: " + function_type.lstrip() 

            function_name = tmp4[-1]
            print "function_name: " + function_name
     
            print "arguments: " + str(tmp3)
            #print tmp3[-2]
            
            tmp31 = tmp3[-2].split(",")
            for num in range(0, len(tmp31)):
                print "   " + tmp31[num].lstrip()
       
                collect.insert( { 'type' : "definition", 'callee' : callee, 'function_type' : function_type.lstrip(), 'function_name' :  function_name, 'location' : location, 'linenumber' : linenumber.strip(), 'arguments' : tmp31[num].lstrip() } )

        except:
            pass

    line = f.readline() 
