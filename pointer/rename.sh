COUNTER=0
for line in `cat ${1}`
do
    #echo "now processing " $line ":" $COUNTER " ..."
    cut=`echo $line | cut -c 4-`
    echo -e $cut "\n"
    #cp $line $COUNTER
    #COUNTER=`expr $COUNTER + 1`
done
