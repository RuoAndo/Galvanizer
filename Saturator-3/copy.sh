#!/bin/bash

# ./listup-full.pl | grep gz > list
# ./copy.sh list

#numLine=1
cat $1 | while read line
do
    cp $line /home/flare/Saturator-codes/httpd/
    #echo $numLine: $line # 出力
    #numLine=$((numLine + 1)) # 行数を1増やす
done
