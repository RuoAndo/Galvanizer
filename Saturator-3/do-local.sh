# usage
# move to target source code directory
# cd xen-4.1.0
# ./do.sh

saturator_minor_version="saturator3-2"
mongodb_ip="127.0.0.1"

gtags -v
./listup.pl > list
./global-t.sh list > flist
./cut.pl flist > flist2
./drem.pl flist2 > flist2-drem
./global-rx.sh flist2-drem > flist3
python global-rx.py flist2-drem > flist3
./flist_to_csv.pl flist > flist.csv
./flist_to_csv.pl flist3 > list-callchain.csv

currentdir=`pwd | awk -F'/' '{print $0}'`
currentdir2=`echo $currentdir | sed -e "s/\-/_/g"`
currentdir3=`echo $currentdir2 | sed -e "s/\//_/g"`
currentdir4=`echo $currentdir3 | sed -e "s/\./_/g"`
pwd3=`echo $currentdir4 | sed -e "s/\//_/g" | cut -c2-`
echo $pwd3

# store 

# functions 
# > db.home_flare_Downloads_xen_4_1_0.find({"function_name" : "libxl_list_cpupool"})
# { "_id" : ObjectId("567a0e2d0dd43c606dde5d3c"), "file_name" : "tools_libxl_libxl__c", "line_number" : 388, "function_name" : "libxl_list_cpupool" }

python store_gtags_f_flist.py flist.csv $saturator_minor_version $pwd3 $mongodb_ip
#python store_gtags_rx_callchain.py list-callchain.csv $saturator_minor_version $pwd3 192.168.11.9

# extracting callchains with numpy

# callers
# > db.home_flare_Downloads_xen_4_1_0.callers.find()
# { "_id" : ObjectId("567a10740dd43c3e140cf8d0"), "caller_line_number" : 155, "file_name" : "extras_mini-os_main__c", "ID_line_number" : 19, "ID_name" : "main", "caller_name" : "environ" }

python extract_callers.py list-callchain.csv $saturator_minor_version $pwd3 $mongodb_ip $mongodb_ip
