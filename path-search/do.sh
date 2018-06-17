#!/bin/sh

TESTFILE=$1
while read line; do
    #echo $line
    ./path.sh $line libxl_list_cpupool 3
    ./path.sh $line libxl_list_cpupool 4
    ./path.sh $line libxl_list_cpupool 5        
done < $TESTFILE
