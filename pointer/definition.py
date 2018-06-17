# usage: python listup.py [dbname] [location(dir path] [line number]
from pymongo import MongoClient

import numpy
import numpy as np
import sys

argvs = sys.argv  
argc = len(argvs) 

software_version = argvs[1]

connect = MongoClient("127.0.0.1", 27017)
db= connect[software_version]
collect = db['definition']

f = open(argvs[2])

line = f.readline() 

while line:
    #print line

    line_number_array = []
    function_name_array = []

    ret = collect.find({"location" : line.strip()})
    if  ret.count() > 0:     
        for doc in ret:
            if doc['linenumber'].isdigit() == True:
                line_number_array.append(int(doc['linenumber']))
                function_name_array.append(str(doc['function_name']))
            
        line_number_array_uniq = list(set(line_number_array))

        print line.strip() + ":" + str(line_number_array_uniq)
        print line.strip() + ":" + str(line_number_array_uniq.sort())
        print line.strip() + ":" + str(function_name_array)

        counter = 0
        for fn in function_name_array:
            try:
                tmp_startln = line_number_array_uniq[counter-1]-1
                tmp_endln = line_number_array_uniq[counter]-1

                print line
                print fn + ":" + str(line_number_array_uniq[counter-1]) + ":" + str(int(line_number_array_uniq[counter]-1))

                
                f2 = open(line.strip(), 'r')
                lines =  f2.readlines()

                fnstr = "fn-" + fn
                f3 = open(fnstr, 'w')

                f3.write(line)
                num = tmp_startln
                while num < tmp_endln:
                    print lines[num].replace("\n","")
                    f3.write(lines[num].replace("\n",""))
                    f3.write("\n")
                    num = num + 1
                f2.close()
                f3.close()
                
            except:
                pass
            counter = counter + 1
        
    line = f.readline()
    
    
