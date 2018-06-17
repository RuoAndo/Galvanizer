while read line; do
    ./parse < $line $line
done < $1
