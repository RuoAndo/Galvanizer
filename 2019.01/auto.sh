time ./listup.pl > list
time ./global-t.sh list > flist
tim3 python 2.py flist > t.csv
time python 1.py flist > flist2
time ./global-rx.sh flist2 > flist3
time python 2.py flist3 > r.csv
