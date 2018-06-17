#apt-get install -y global
gtags -v

#./listup.pl > list 
#./global-t.sh list > flist
#./1.pl flist > flist2
#./cut.pl flist2 > flist3
#./drem.pl flist3 > flist3-drem
#python global-rx.py flist3-drem > flist4

./listup.pl | tee list 
./global-t.sh list | tee flist
./1.pl flist | tee flist2
./cut.pl flist2 | tee flist3
./drem.pl flist3 | tee flist3-drem
#python global-rx.py flist3-drem | tee flist4
#./1.pl flist4 > flist5
