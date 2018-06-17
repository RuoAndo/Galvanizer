apt-get install -y wget
apt-get install -y gcc g++
apt-get install -y ncurses-dev
apt-get install -y global

#wget ftp://ftp.gnu.org/pub/gnu/global/global-6.5.5.tar.gz
#tar zxvf global-6.5.5.tar.gz
#yum install -y ncurses ncurses-devel ncurses-libs
#cd global-6.5.5
#./configure 
#make 
#make install

PATH=$PATH:/usr/local/bin
export PATH

#cd ..

rm -rf bind-9.6.1-P1.tar.gz
rm -rf bind-9.6.1-P1
wget ftp://ftp.isc.org/isc/bind9/9.6.1-P1/bind-9.6.1-P1.tar.gz
tar zxvf bind-9.6.1-P1.tar.gz
\cp -f makelist.sh *py *pl *sh ./bind-9.6.1-P1/

\cp -f postgres/* ./bind-9.6.1-P1/

#cp makelist.sh *py *pl *sh ./bind-9.6.1-P1/
#cp makelist.sh *py *pl *sh ./bind-9.6.1-P1/
#cp makelist.sh *py *pl *sh ./bind-9.6.1-P1/
cd bind-9.6.1-P1

currentdir=`pwd | awk -F'/' '{print $0}'`
echo $currentdir

array=( `echo $currentdir | tr -s '/' ' '`)
last_index=`expr ${#array[@]} - 1`

# print fuga
echo ${array[${last_index}]}

currentdir=${array[${last_index}]}

currentdir2=`echo $currentdir | sed -e "s/\-//g"`
echo $currentdir2

currentdir3=`echo $currentdir2 | sed -e "s/\///g"`
echo $currentdir3

currentdir4=`echo $currentdir3 | sed -e "s/\.//g"`
echo $currentdir4

chmod 755 *pl
chmod 755 *py
chmod 755 *sh
gtags -v
rm -rf list
./listup.pl | tee list
rm -rf flist
./global-t.sh list | tee flist
rm -rf flist2 
./1.pl flist | tee list-definition-$currentdir4
rm -rf flist3 
./cut.pl list-definition-$currentdir4 | tee flist3
rm -rf flist3-drem 
./drem.pl flist3 | tee flist3-drem
rm -rf flist4
python global-rx.py flist3-drem | tee flist4
rm -rf flist5
./1.pl flist4 | tee list-callchain-$currentdir4

