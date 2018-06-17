# usage: ./find4.sh x411_func_dump_drem

saturator_minor_version="saturator3-2"
mongodb_ip="127.0.0.1"
collection_name="root_memcached_tarballs_memcached_1_4_16"

TESTFILE=$1
while read line; do

    date=`date +"%Y_%m_%d_%I_%M_%S"`
    touch $line-$date
    #echo $line
    python find4.py $mongodb_ip $saturator_minor_version $collection_name $line 2 | tee $line-$date.func
    
    dot -Tpng $line-$date.func -o $line-$date.png
    pkill eog
    eog $line-$date.png &

done < $TESTFILE
