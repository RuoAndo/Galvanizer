#!/bin/sh
echo $1
filename=$1

while read LINE; do
global -f ${LINE}
done < ${filename}

