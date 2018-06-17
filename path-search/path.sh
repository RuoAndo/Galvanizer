#python ex-list.py $1 $2 $3 | tee tmp
python ex-list.py $1 $2 $3 > tmp
wc=`wc -l tmp`

#echo $wc

pram=`echo $wc | cut -d " " -f 1`
gc=`grep EMPTY tmp | wc -l`
echo $1 ":" $2 ":" $3 ":" $gc ":" $pram
