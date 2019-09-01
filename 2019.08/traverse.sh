nLines=100000

./build-traverse.sh traverse2

rm -rf rx-*

#find . -maxdepth 1 -type d | grep '[a-z]' | grep -v Document | cut -c 3- > list 
find . -maxdepth 1 -type d | grep '[a-z]' | grep -v Document | grep ipc | cut -c 3- > list 

rm -rf stats
touch stats

wc -l r.csv
while read line; do
    echo $line
    time grep $line r.csv > r.csv.${line}
    wc -l r.csv.${line}

    mkdir rx-${line}
    split -l $nLines r.csv.${line}
    mv x* ./rx-${line}/

    nFiles=`ls ./rx-${line}/ | wc -l | cut -d " " -f 1`
    echo $line" - # of files:"$nFiles

    SECONDS=0
    time ./traverse2 rx-${line} t.csv
    time=$SECONDS

    wLines=`wc -l r.csv.${line} | wc -l | cut -d " " -f 1`

    echo ${line}","${wLines}","${nFiles}","${time} >> stats

    echo " "
done < list
