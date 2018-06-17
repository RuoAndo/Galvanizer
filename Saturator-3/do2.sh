#pwd=`pwd | awk -F'/' '{print $NF}'`
#pwd2=`echo $pwd | sed -e "s/\./_/g"`
#pwd3=`echo $pwd2 | sed -e "s/\-/_/g"`
#echo $pwd3

currentdir=`pwd | awk -F'/' '{print $0}'`
currentdir2=`echo $currentdir | sed -e "s/\-/_/g"`
currentdir3=`echo $currentdir2 | sed -e "s/\//_/g"`
currentdir4=`echo $currentdir3 | sed -e "s/\./_/g"`
pwd3=`echo $currentdir4 | sed -e "s/\//_/g" | cut -c2-`
echo $pwd3

gtags -v
../listup.pl > list
../global-t.sh list > flist
../cut.pl flist > flist2
../drem.pl flist2 > flist2-drem
../global-rx.sh flist2-drem > flist3
python ../global-rx.py flist2-drem > flist3
../flist_to_csv.pl flist > flist.csv
../flist_to_csv.pl flist3 > list-callchain.csv

# store 
python ../store_gtags_f_flist.py flist.csv saturator3 $pwd3 192.168.11.9
python ../store_gtags_rx_callchain.py list-callchain.csv saturator3 $pwd3 192.168.11.9

# numpy
python ../csvread.py list-callchain.csv saturator3 $pwd3 192.168.11.9 192.168.11.9
