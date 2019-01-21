time ./listup.pl > list
time ./global-t.sh list > flist
time python 1.py flist > flist2
time ./global-rx.sh flist2 > flist3
