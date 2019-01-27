rm -rf a.out
g++ -c csv.cpp -std=c++11
g++ -g -o $1 $1.cpp csv.o -std=c++11


