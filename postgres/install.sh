apt-get install -y postgresql
apt-get install -y python-psycopg2
cp pg_hba.conf /etc/postgresql/9.5/main/pg_hba.conf
python createdb.py
python pg_stat_database.py     
