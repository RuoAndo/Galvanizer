saturator_minor_version="saturator9-1"
mongodb_ip="192.168.11.9"

pwdorg=`pwd`

TESTFILE=$1
while read line; do

    if [ `echo $line | grep "\/\."` ]; then
	continue
    fi

    pwd=`pwd`
    currentdir2=`echo $line |  awk -F'\.tar.gz' '{print $1}'`
    echo "current dir2" $currentdir2
    tar zxvf $line #-C $currentdir

    cd $currentdir2
    pwd=`pwd`
    echo $pwd

    currentdir=`pwd | awk -F'/' '{print $0}'`
    currentdir2=`echo $currentdir | sed -e "s/\-/_/g"`
    currentdir3=`echo $currentdir2 | sed -e "s/\//_/g"`
    currentdir4=`echo $currentdir3 | sed -e "s/\./_/g"`
    pwd3=`echo $currentdir4 | sed -e "s/\//_/g" | cut -c2-`
    echo $pwd3

    gtags -v
    $pwdorg/listup.pl > list
    $pwdorg/global-t.sh list > flist
    $pwdorg/cut.pl flist > flist2
    $pwdorg/drem.pl flist2 > flist2-drem
    #\cp -f flist2-drem $pwd/
    $pwdorg/global-rx.sh flist2-drem > flist3
    $pwdorg/flist_to_csv.pl flist > flist.csv
    $pwdorg/flist_to_csv.pl flist3 > list-callchain.csv

    # store 
    python $pwdorg/store_gtags_f_flist.py flist.csv $saturator_minor_version $pwd3 $mongodb_ip
    python $pwdorg/store_gtags_rx_callchain.py list-callchain.csv $saturator_minor_version $pwd3 $mongodb_ip

    # numpy
    python $pwdorg/csvread.py list-callchain.csv $saturator_minor_version $pwd3 $mongodb_ip $mongodb_ip

    cd $pwdorg

done < $TESTFILE
