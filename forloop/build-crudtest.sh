#g++ -g -Wall -I/usr/local/include -L/usr/local/lib -lmongoclient CrudTest.cpp
g++ CrudTest.cpp -pthread -lmongoclient -lboost_thread -lboost_system -lboost_regex -o CrudTest
