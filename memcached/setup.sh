apt-get update -y
apt-get install -y memcached
apt-get install -y python-memcache

yum install -y libmemcached.x86_64
yum install -y python-memcached
yum install -y memcached.x86_64
service memcached start

curl -kL https://bootstrap.pypa.io/get-pip.py | python
pip install pymongo
pip install numpy
#pip install python-memcached
