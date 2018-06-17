# definition.py

# libxl_ctx_free:int libxl_ctx_free(libxl_ctx *ctx):libxl.c:79
# libxl_string_list_destroy:void libxl_string_list_destroy(libxl_string_list *psl):libxl.c:87
# dns_diff_load:dns_diff_load(dns_diff_t *diff, dns_addrdatasetfunc_t addfunc,void *add_private):lib/dns/diff.c:442

# sql = "create TABLE definition(id INT, software_version varchar(1024), linktype varchar(1024), function_type varchar(1024), function_name varchar(1024), location varchar(1024), linenumber INT);"

#1 id : 1 
#2 software_version : bind998
#3 linktype : definition
#4 function_type : void, int ..
#5 function_name : libxl_string_list_destroy(libxl_string_list *psl)
#6 location : lib/dns/diff.c
#7 linenumber : 443

import sys 
import psycopg2

argvs = sys.argv  
argc = len(argvs) 

f = open(argvs[1])
software_version = argvs[2]
dbname = argvs[2]

array = []
counter = 0

conn = psycopg2.connect(
    host = "127.0.0.1",
    port = 5432,
    database=dbname,
    user="postgres",
    password="")

cur = conn.cursor()

try:
    sql = "drop TABLE definition;"
    cur.execute(sql)
    cur.commit()
except:
    print "cur error"
    cur.close()
 
cur2 = conn.cursor()

try:
    sql = "create TABLE definition(id INT, software_version varchar(1024), linktype varchar(1024), function_type varchar(1024), function_name varchar(1024), location varchar(1024), linenumber INT);"

    cur2.execute(sql)
    cur2.commit()

except:
    print "cur2 error"
    cur2.close()

line = f.readline() 

counter = 0

while line:

    print "-------------"

    print line

    if line.find('(') > -1 and line.find(')') > -1:

        cur3 = conn.cursor()

        try:
            #uint64_t vhash(unsigned char m[],vmac_ctx_t *ctx):xen/crypto/vmac.c:846

            print line

            tmp = line.split("(")
            tmp3 = line.split(":")

            tmp21 = tmp[0].split(":")
            tmp2 = tmp21[1].split()
            
            function_type = "default"
            for num in range(0, len(tmp2)-1):
                ##
                function_type = function_type + " " + str(tmp2[num])

            ##    
            function_name = tmp2[-1]
            print "function_name:" + function_name
            print "function_type:" + function_type
       
            tmp4 = tmp[1].split(")")
            print "arguments:" + tmp4[0]
            arguments = tmp4[0]

            print "location:" + tmp3[2]

            ##
            location = tmp3[2]
            print "linenumber:" + tmp3[3]

            ##
            linenumber = 0
            linenumber = int(tmp3[3].rstrip())

            listtype = "definition"
            
            ########
            print "#### function ####"
            print "software_version:" + software_version
            print "type:" + listtype
            print "function_type:" + function_type.lstrip()
            print "function_name:" + function_name
            print "location:" + location
            print "linenumber:" + str(linenumber)
            print "####  #### ### ###"

            
            #sql = "INSERT INTO definition (id, software_version, type, function_type, function_name, location, linenumber) VALUES (" + str(counter) + ", '" + software_version + "', '" + type + "', '" + function_name + "', '" + location + "', '" + linenumber +"');"

            sql = "INSERT INTO definition (id, software_version, linktype, function_type, function_name, location, linenumber) VALUES (" + str(counter) + ", '" + software_version + "', '" + listtype + "', '" + function_type + "', '" + function_name + "', '" + location + "', '" + str(linenumber) +"');"

            print sql

            cur3.execute(sql)
            conn.commit()
                        
            # splitting arguments
            arg_tmp = tmp4[0].split(",")
            print arg_tmp
            for i in arg_tmp:
                arg_tmp_2 = i.lstrip()
                arg_tmp_3 = arg_tmp_2.split(" ")
                arg_type = ""
                for num in range(0, len(arg_tmp_3)-1):
                    arg_type = arg_type + " " + str(arg_tmp_3[num])
                    
                print arg_type + ":" + arg_tmp_3[-1]

        except:
            print "cur3 error"
            cur3.close()
            pass

    counter = counter + 1
    line = f.readline() 

conn.close()
