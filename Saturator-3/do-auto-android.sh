pwdorg=`pwd`

saturator_minor_version="saturator3-jadx-101"                                                                        
mongodb_ip="192.168.11.7"

TESTFILE=$1
while read line; do

    #cd $currentdir
    pwd=`pwd`
    echo $pwd/$line

    targetdir=`echo $line |  awk -F'\.apk' '{print $1}'`
    rm -rf $targetdir


    timeout 120 /home/flare/jadx/build/jadx/bin/jadx $pwd/$line
    #timeout 120 jadx $pwd/$line


    cd $targetdir

    #currentdir=`pwd | awk -F'/' '{print $0}'`
    #currentdir2=`echo $currentdir | sed -e "s/\-/_/g"`
    #currentdir3=`echo $currentdir2 | sed -e "s/\//_/g"`
    #currentdir4=`echo $currentdir3 | sed -e "s/\./_/g"`
    #pwd3=`echo $currentdir4 | sed -e "s/\//_/g" | cut -c2-`
    #echo $pwd3

    \cp /home/flare/Saturator-3/* ./
    ./do-android.sh $saturator_minor_version $mongodb_ip

    cd $pwdorg

    #gtags -v
    #$pwdorg/listup.pl > list
    #$pwdorg/global-t.sh list > flist
    #$pwdorg/cut.pl flist > flist2
    #$pwdorg/drem.pl flist2 > flist2-drem
    #\cp -f flist2-drem $pwd/
    #$pwdorg/global-rx.sh flist2-drem > flist3
    #$pwdorg/flist_to_csv.pl flist > flist.csv
    #$pwdorg/flist_to_csv.pl flist3 > list-callchain.csv

done < $TESTFILE
