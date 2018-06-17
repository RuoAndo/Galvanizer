apt-get install -y wget
apt-get install -y gcc g++
apt-get install -y ncurses-dev
apt-get install -y global
apt-get install -y python

apt-get install -y mongodb-clients
apt-get install -y mongodb-server
apt-get install -y python-psycopg2

apt-get install -y python-pymongo
apt-get install -y python-pip
pip install numpy

make

PATH=$PATH:/usr/local/bin
export PATH

rm -rf list-mongodb-xen
./listup.pl | grep gz | grep tar > list

date=`date '+%y_%m_%d_%H_%M_%S'`

TESTFILE=list

while read line; do
    
    cp $line .

    tar zxvf $line
    
    array=( `echo $line | tr -s '/' ' '`)
    last_index=`expr ${#array[@]} - 1`
    echo ${array[${last_index}]}
    d=`echo ${array[${last_index}]} | sed s/.tar.gz//g`
    #echo $d

    cp listup.pl $d/
    cp parse $d/
    cd $d

    ./listup.pl > list2
    
    currentdir=`pwd | awk -F'/' '{print $0}'`
    echo $currentdir
    array=( `echo $currentdir | tr -s '/' ' '`)
    last_index=`expr ${#array[@]} - 1`
    echo ${array[${last_index}]}
    currentdir=${array[${last_index}]}
    currentdir2=`echo $currentdir | sed -e "s/\-//g"`
    currentdir3=`echo $currentdir2 | sed -e "s/\///g"`
    currentdir4=`echo $currentdir3 | sed -e "s/\.//g"`
    echo $currentdir4
    
    TESTFILE=list2
    while read line; do

	currentdir=`pwd | awk -F'/' '{print $0}'`
	array=( `echo $currentdir | tr -s '/' ' '`)
	last_index=`expr ${#array[@]} - 1`
	currentdir=${array[${last_index}]}
	currentdir2=`echo $currentdir | sed -e "s/\-//g"`
	currentdir3=`echo $currentdir2 | sed -e "s/\///g"`
	currentdir4=`echo $currentdir3 | sed -e "s/\.//g"`
	echo $currentdir4

	line2=`echo $line | cut -c 3-`
	echo $line2

	if [ `echo $line2 |grep parse` ]; then
	    echo "skip"
	else
	    echo "line:" $line
	    echo "line2:" $line2
	    echo $currentdir4
	    ./parse < $line2 $line2 $currentdir4
	fi
    
    done < $TESTFILE

done < $TESTFILE


