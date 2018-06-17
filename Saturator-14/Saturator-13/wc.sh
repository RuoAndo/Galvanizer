saturator_minor_version="saturator9-1"
mongodb_ip="192.168.11.9"

pwdorg=`pwd`

TESTFILE=$1
while read line; do

    if [ `echo $line | grep "\/\."` ]; then
	continue
    fi

    wc -l $line

done < $TESTFILE
