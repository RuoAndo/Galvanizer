#!/bin/sh
echo $1
filename=$1

while read LINE; do
global -rx ${LINE}
#sleep 1 
#wait
done < ${filename}

