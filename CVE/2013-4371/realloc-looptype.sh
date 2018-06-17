TESTFILE=$1
while read line; do
    ./parse < $line $line
done < $TESTFILE
