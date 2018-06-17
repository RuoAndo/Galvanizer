saturator_minor_version="saturator13-xen"
mongodb_ip="192.168.11.2"

pwdorg=`pwd`
make

#python dropdatabase.py $mongodb_ip $saturator_minor_version

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

    $pwdorg/listup.pl > list
    LD_LIBRARY_PATH=/usr/local/lib:/usr/lib 
    export LD_LIBRARY_PATH
    $pwdorg/listup.pl > list

    # parsing forloop

    # bison-parser.sh
    # if [ ` echo $line |grep "\.c"` ]; then
    # echo $line
    # $pwdorg/parser < $line $line $colname $pwd3"_func" $ip_address
    # fi

    # 2016-05-10-13-09
    cp $pwdorg/parser .
    $pwdorg/bison-parser.sh list $saturator_minor_version $mongodb_ip

    pwd=`pwd | awk -F'/' '{print $NF}'`
    pwd4=`echo $pwd | sed -e "s/\./_/g"`
    pwd5=`echo $pwd4 | sed -e "s/\-/_/g"`
    echo $pwd5

    # extracting caller function of forloop(s)

    cp $pwdorg/1.py .
    python 1.py $mongodb_ip $saturator_minor_version $pwd5

    cd $pwdorg

done < $TESTFILE
