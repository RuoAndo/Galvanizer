#rm -rf processing_time
#touch processing_time

currentdir=`pwd | awk -F'/' '{print $0}'`
echo $currentdir

array=( `echo $currentdir | tr -s '/' ' '`)
last_index=`expr ${#array[@]} - 1`

echo ${array[${last_index}]}
currentdir=${array[${last_index}]}
currentdir2=`echo $currentdir | sed -e "s/\-//g"`
echo $currentdir2
currentdir3=`echo $currentdir2 | sed -e "s/\///g"`
echo $currentdir3
currentdir4=`echo $currentdir3 | sed -e "s/\.//g"`
echo $currentdir4

TIME_A=`date +%s`   #A

sleep 1

TIME_B=`date +%s`   #B
PT=`expr ${TIME_B} - ${TIME_A}`
H=`expr ${PT} / 3600`
PT=`expr ${PT} % 3600`
M=`expr ${PT} / 60`
S=`expr ${PT} % 60`
proctime=`echo "${H}:${M}:${S}"`

echo $currentdir4 ":" $proctime >> processing_time 
