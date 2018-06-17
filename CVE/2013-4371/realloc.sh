TESTFILE=$1
while read line; do
    python realloc.py $line
done < $TESTFILE