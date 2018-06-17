saturator_minor_version="saturator3-1"
mongodb_ip="127.0.0.1"

currentdir=`pwd | awk -F'/' '{print $0}'`
currentdir2=`echo $currentdir | sed -e "s/\-/_/g"`
currentdir3=`echo $currentdir2 | sed -e "s/\//_/g"`
currentdir4=`echo $currentdir3 | sed -e "s/\./_/g"`
pwd3=`echo $currentdir4 | sed -e "s/\//_/g" | cut -c2-`
echo $pwd3

depth=$2
depth2=$3

collection_name=$pwd3".callers"

date=`date +"%Y_%m_%d_%I_%M_%S"`
python find4.py $mongodb_ip $saturator_minor_version $collection_name $1 $depth | tee $1-$date.func

python find7.py $mongodb_ip $saturator_minor_version $collection_name $1 $depth2 | tee -a $1-$date.func

echo "}" >> $1-$date.func

rm -rf tmpdot
cp $1-$date.func tmpdot

dot -Tpng $1-$date.func -o $1-$date-depth-$2-$3.png
mv $1-$date-depth-$2-$3.png /var/www/html/images/

dot -Tpng tmpdot -o tmpdot.png
rm -rf /var/www/html/images/tmpdot.png
mv tmpdot.png /var/www/html/images/