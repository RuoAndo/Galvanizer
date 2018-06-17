# usage: 
# cd DIR : move target directory
# ls | grep apk > list
# ./do-auto-android-viz.sh list

pwdorg=`pwd`

TESTFILE=$1
while read line; do

    pwd=`pwd`
    echo $pwd/$line

    targetdir=`echo $line |  awk -F'\.apk' '{print $1}'`
    rm -rf $targetdir

    cd $targetdir

    #cp /root/Saturator-3/* ./
    cp ~/Saturator-3/* ./
    ./viz-android.sh

    cd $pwdorg

done < $TESTFILE
