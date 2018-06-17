yum install -y postgresql-server
yum install -y python-psycopg2  
yum install -y emacs screen
service postgresql initdb
service postgresql start
echo "createdb sample"                                                                    
sudo -u postgres createdb sample  
\cp -f postgres/pg_hba.conf /var/lib/pgsql/data/pg_hba.conf
service postgresql restart
python postgres/pg_stat_database.py

yum install -y wget
yum install -y gcc g++

wget ftp://ftp.gnu.org/pub/gnu/global/global-6.5.5.tar.gz
tar zxvf global-6.5.5.tar.gz
yum install -y ncurses ncurses-devel ncurses-libs
cd global-6.5.5
./configure 
make 
make install

PATH=$PATH:/usr/local/bin
export PATH

cd ..

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
./makelist.sh

curl -kL https://bootstrap.pypa.io/get-pip.py | python
pip install pymongo
pip install numpy

./insert.sh

######
cd ..
#rm -rf linux-2.6.0.tar.gz
#rm -rf linux-2.6.0
#wget https://www.kernel.org/pub/linux/kernel/v2.6/linux-2.6.0.tar.gz
#tar zxvf linux-2.6.0.tar.gz
#\cp -f makelist.sh *py *pl *sh ./linux-2.6.0

#\cp -f postgres/* ./linux-2.6.0

#cd linux-2.6.0
#./makelist.sh
#./insert.sh
