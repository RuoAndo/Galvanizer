CFLAGS = -g 

all:	  parse

# reentrant flex and bison

parse:	parse.lex.o parse.tab.o sat-ctx.o
	c++ -g -o $@ parse.lex.o parse.tab.o sat-ctx.o -lm -lmongoclient -lboost_thread -lboost_system -lboost_regex

parse.lex.o: parse.lex.c parse.tab.hh 
	c++ -g -c -I/usr/local/include/libbson-1.0 -I/usr/local/include/libmongoc-1.0 -lmongoclient -lboost_thread -lboost_system -lboost_regex $<

parse.tab.o: parse.tab.cc  
	c++ -g -c -I/usr/local/include/libbson-1.0 -I/usr/local/include/libmongoc-1.0 -lmongoclient -lboost_thread -lboost_system -lboost_regex $<

sat-ctx.o: sat-ctx.cpp

parse.lex.c: parse.l
	flex -oparse.lex.c parse.l

parse.tab.cc parse.tab.hh: parse.yy 
	bison -vd parse.yy

clean:
	rm -f parse \
	parse.lex.c parse.tab.c parse.tab.cc parse.tab.hh \
	parse.lex.o parse.tab.o parse.output sat-ctx.o \
	location.hh position.hh stack.hh *~ \#*
