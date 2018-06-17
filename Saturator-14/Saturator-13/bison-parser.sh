#!/bin/sh
# ファイルを1行ずつ読み込んで表示

pwd=`pwd | awk -F'/' '{print $NF}'`
pwd2=`echo $pwd | sed -e "s/\./_/g"`
pwd3=`echo $pwd2 | sed -e "s/\-/_/g"`
echo $pwd3

colname=$2
ip_address=$3

pwdorg=`pwd`

TESTFILE=$1
while read line; do

    if [ ` echo $line |grep "\.c"` ]; then
	echo $line
	$pwdorg/parser < $line $line $colname $pwd3"_func" $ip_address
    fi

    if [ ` echo $line |grep "\.h"` ]; then
	echo $line
	$pwdorg/parser < $line $line $colname $pwd3"_func" $ip_address
    fi

    if [ ` echo $line |grep "\.hh"` ]; then
	echo $line
	$pwdorg/parser < $line $line $colname $pwd3"_func" $ip_address
    fi

    if [ ` echo $line |grep "\.cpp"` ]; then
	echo $line
	$pwdorg/parser < $line $line $colname $pwd3"_func" $ip_address
    fi

    if [ ` echo $line |grep "\.txt"` ]; then
	echo $line
	$pwdorg/parser < $line $line $colname $pwd3"_func" $ip_address
    fi

done < $TESTFILE
