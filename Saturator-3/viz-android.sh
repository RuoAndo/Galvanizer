mongoip="192.168.11.9"

# should be same as do.sh
saturator_minor_version="saturator3-1"

currentdir=`pwd | awk -F'/' '{print $0}'`
currentdir2=`echo $currentdir | sed -e "s/\-/_/g"`
currentdir3=`echo $currentdir2 | sed -e "s/\//_/g"`
currentdir4=`echo $currentdir3 | sed -e "s/\./_/g"`
pwd3=`echo $currentdir4 | sed -e "s/\//_/g" | cut -c2-`
echo $pwd3


rm -rf files
mkdir files
./cut2.pl flist.csv > funclist

TESTFILE=funclist
while read line; do

    date=`date +"%Y_%m_%d_%I_%M_%S"`
    touch $line-$date
    python viz-android.py $mongoip $saturator_minor_version $pwd3 $line 2 | tee $line-$date.func
    
    dot -Tpng $line-$date.func -o $line-$date.png
    pkill eog
    eog $line-$date.png &
    sleep 5
done < $TESTFILE
