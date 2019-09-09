nLines=100000

./build-traverse.sh traverse2

rm -rf rx-*

#find . -maxdepth 1 -type d | grep '[a-z]' | grep -v Document | cut -c 3- > list 
find . -maxdepth 1 -type d | grep '[a-z]' | grep -v Document | grep -v driver | cut -c 3- > list 

rm -rf stats
touch stats

wc -l r.csv
while read line; do
    echo $line
    time grep $line r.csv > r.csv.${line}
    rLines=`wc -l r.csv.${line} | cut -d " " -f 1`
    echo $rLines
    
    mkdir rx-${line}
    split -l $nLines r.csv.${line}
    mv x* ./rx-${line}/

    nFiles=`ls ./rx-${line}/ | wc -l | cut -d " " -f 1`
    echo $line" - # of files:"$nFiles

    #SECONDS=0
    start_time=`date +%s`
    time ./traverse2 rx-${line} t.csv
    #time=$SECONDS
    end_time=`date +%s`
    time=$((end_time - start_time))
    
    wLines=`wc -l r.csv.${line} | wc -l | cut -d " " -f 1`
    fLines=`grep ${line} t.csv | wc -l | cut -d " " -f 1`

    echo ${line}","${rLines}","${fLines}","${time} >> stats

    echo " "
done < list
