# usage: ./do.sh 1
# option 0 avoids makelist block below.

if [ $1 -ne 0 ]
then
./makelist.sh
fi

#####

PATH=$PATH:/usr/local/bin
export PATH

currentdir=`pwd | awk -F'/' '{print $0}'`
echo $currentdir

array=( `echo $currentdir | tr -s '/' ' '`)
last_index=`expr ${#array[@]} - 1`

# print fuga
echo ${array[${last_index}]}

currentdir=${array[${last_index}]}

currentdir2=`echo $currentdir | sed -e "s/\-//g"`
echo $currentdir2

currentdir3=`echo $currentdir2 | sed -e "s/\///g"`
echo $currentdir3

currentdir4=`echo $currentdir3 | sed -e "s/\.//g"`
echo $currentdir4

#####

python flist2.py flist2 list-definition-$currentdir4
python flist5.py flist5 list-callchain-$currentdir4
python ex3.py $currentdir4
