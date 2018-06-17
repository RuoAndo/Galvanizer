TESTFILE=$1
while read line; do
    python for.py $line
done < $TESTFILE