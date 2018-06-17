# install

<pre>

apt-get install -y flex bison cmake scons
apt-get install -y libboost-all-dev

git clone https://github.com/mongodb/libbson.git
cd libbson/
cmake CMakeLists.txt
time make
make install

cd ..

git clone https://github.com/mongodb/mongo-c-driver.git
ls
cd mongo-c-driver/
cmake CMakeLists.txt
time make
time make install

cd ..

git clone https://github.com/mongodb/mongo-cxx-driver.git
cd mongo-cxx-driver/
git checkout legacy
scons --disable-warnings-as-errors --prefix=/usr/local
scons --disable-warnings-as-errors --prefix=/usr/local install

</pre>

avoid warnings about "_theGlobalInitializer" by adding the flag --disable-warnings-as-errors to your SCons invocation. see: https://groups.google.com/forum/#!topic/mongodb-user/5_v7jlgGM2I

<pre>

scons --disable-warnings-as-errors --prefix=/usr/local
scons --disable-warnings-as-errors --prefix=/usr/local install

</pre>