DIR=$1

cp ./listup.pl $DIR

cd $DIR

#gtags -v
#cd ..

./listup.pl > list

rm -rf all
touch all

while read line; do
    global -f $line >> all
done < list
