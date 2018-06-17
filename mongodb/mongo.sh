curl -kL https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python 
pip install pymongo numpy

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

python flist2.py list-definition-$currentdir4 $currentdir4
python flist5.py list-callchain-$currentdir4 $currentdir4
python ex3.py $currentdir4
