sapt-get install -y wget
apt-get install -y gcc g++
apt-get install -y ncurses-dev
apt-get install -y global
apt-get install -y python

apt-get install -y mongodb-clients
apt-get install -y mongodb-server
apt-get install -y python-psycopg2

PATH=$PATH:/usr/local/bin
export PATH

./listup.pl | grep gz | grep xen | grep tar > postgres_xen_list
#./listup.pl | grep gz | grep xen | grep 3.3.0 >> postgres_xen_list

date=`date '+%y_%m_%d_%H_%M_%S'`
touch processing_time_postgres_xen_$date

TESTFILE=postgres_xen_list
while read line; do
    cp $line .
    array=( `echo $line | tr -s '/' ' '`)
    last_index=`expr ${#array[@]} - 1`
    echo ${array[${last_index}]}
    d=`echo ${array[${last_index}]} | sed s/.tar.gz//g`
    echo $d

    tar zxvf ${array[${last_index}]}

    cp *py *pl *sh *py ./$d/
    cd $d

    currentdir=`pwd | awk -F'/' '{print $0}'`
    echo $currentdir

    array=( `echo $currentdir | tr -s '/' ' '`)
    last_index=`expr ${#array[@]} - 1`

    echo ${array[${last_index}]}
    currentdir=${array[${last_index}]}
    currentdir2=`echo $currentdir | sed -e "s/\-//g"`
    echo $currentdir2
    currentdir3=`echo $currentdir2 | sed -e "s/\///g"`
    echo $currentdir3
    currentdir4=`echo $currentdir3 | sed -e "s/\.//g"`
    echo $currentdir4

    python insert-pair-ryaku-mongo.py $d $currentdir4
    TIME_A=`date +%s` 
    
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

    cp list-definition-$currentdir4 ../
    cp list-callchain-$currentdir4 ../
    cd ..

    cd $d

    curl -kL  https://bootstrap.pypa.io/get-pip.py | python 
    pip install pymongo numpy

    currentdir=`pwd | awk -F'/' '{print $0}'`
    echo $currentdir

    array=( `echo $currentdir | tr -s '/' ' '`)
    last_index=`expr ${#array[@]} - 1`

    echo ${array[${last_index}]}
    currentdir=${array[${last_index}]}
    currentdir2=`echo $currentdir | sed -e "s/\-//g"`
    echo $currentdir2
    currentdir3=`echo $currentdir2 | sed -e "s/\///g"`
    echo $currentdir3

    currentdir4=`echo $currentdir3 | sed -e "s/\.//g"`
    echo $currentdir4

    python dropdb.py $currentdir4
    python createdb.py $currentdir4

    python create_definition.py $currentdir4
    python create_callchain.py $currentdir4
    python create_ex.py $currentdir4

    python definition.py list-definition-$currentdir4 $currentdir4
    python callchain.py list-callchain-$currentdir4 $currentdir4
    python ex.py $currentdir4
    
    #python flist2.py list-definition-$currentdir4 $currentdir4
    #python flist5.py list-callchain-$currentdir4 $currentdir4
    #python ex3.py $currentdir4

    TIME_B=`date +%s`   #B
    PT=`expr ${TIME_B} - ${TIME_A}`
    H=`expr ${PT} / 3600`
    PT=`expr ${PT} % 3600`
    M=`expr ${PT} / 60`
    S=`expr ${PT} % 60`
    proctime=`echo "${H}:${M}:${S}"`

    mongo_counter=`python count.py $currentdir4`
    
    cd ..

    echo $currentdir4 ":" $mongo_counter ":" $proctime >> processing_time_postgres_xen_$date
    
done < $TESTFILE
