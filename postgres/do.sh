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

python drop_definition.py
python drop_callchain.py
python drop_ex.py

python create_definition.py
python create_callchain.py
python create_ex.py

python definition.py list-definition-$currentdir4 $currentdir4
python callchain.py list-callchain-$currentdir4 $currentdir4
python ex.py $currentdir4
