#!/bin/bash

pwd=`pwd`

files="$pwd/*"
fileary=()
dirary=()
for filepath in $files; do
  if [ -f $filepath ] ; then
    fileary+=("$filepath")
  elif [ -d $filepath ] ; then
    dirary+=("$filepath")
  fi
done

#echo "ファイル一覧"
#for i in ${fileary[@]}; do
#  echo $i
#done

#echo "ディレクトリ一覧"
for i in ${dirary[@]}; do
  echo $ii
  cd $i
  cp ../do2.sh .
  ./do2.sh
done
