# python 1.py tools/libxl/libxl.c libxl 372

import sys 

argvs = sys.argv  
argc = len(argvs) 

f = open(argvs[1])

try:
# search word
    fn = argvs[1]
    sw = argvs[2]
    swline = argvs[3]

except:
    pass

line = f.readline() 

linecounter = 1
found_flag_1 = 0
found_flag_2 = 0

while line:

    # libxl_domain_info  372 tools/libxl/libxl.c int libxl_domain_info(libxl_ctx *ctx, 
    # libxl_dominfo *info_r,
    try:

        if line.find(sw) > -1 and line.find("define") == -1:
            if int(swline) == linecounter:
                #print "TEST:" + line
                found_flag_1 = 1
                line2 = line

                if line.find(")") > -1:
                    line = line.replace('\n','')
                    line = line.replace('\r','')
                    print sw + ":" + line.lstrip().rstrip() + ":" + fn + ":" + str(linecounter) 
                
                else:

                    while line:
                        line = f.readline() 
                        line = line.replace('\n','')
                        line = line.replace('\r','')
                        if line.find(")") > -1:
                            line2 = line2.rstrip().lstrip() + line.lstrip().rstrip()
                            line2 = line2.replace('\n','')
                            line2 = line2.replace('\r','')
                            print sw + ":" + line2.lstrip().rstrip() + ":" + fn + ":" + str(linecounter) 
                            found_flag_2 == 1
                            break

    except:
        pass

    linecounter = linecounter + 1
    line = f.readline() 
