TARGET = parser
BISON_SRC = parse.y
BISON_H   = parse.tab.h parse.c
BISON_C   = parse.tab.c 
BISON_O   = parse.tab.o
BISON_OUT = $(BISON_C) $(BISON_H) $(TARGET).output
FLEX_SRC  = parse.l
FLEX_C    = lex.yy.c
FLEX_O    = lex.yy.o
C_FILES   = $(BISON_C) $(FLEX_C)  
OBJ       = $(FLEX_O) $(BISON_O)

all : $(TARGET)

$(TARGET) : $(OBJ)
	gcc -g -pg -o $@ $(OBJ) -lfl -Wall -lmongoc-1.0 -lbson-1.0 -L/usr/local/lib -I/usr/local/include/libmongoc-1.0/ -I/usr/local/include/libbson-1.0/

$(FLEX_C) : $(FLEX_SRC) $(BISON_H)
	flex $(FLEX_SRC)

$(BISON_OUT) : $(BISON_SRC)
	bison -dv $(BISON_SRC)

.c.o :
	gcc -g -pg -c -lfl -Wall -lmongoc-1.0 -lbson-1.0 -L/usr/local/lib -I/usr/local/include/libmongoc-1.0/ -I/usr/local/include/libbson-1.0/ $<

clean :
	rm -f $(TARGET)
	rm -f lex.yy.c parse.tab.c
	rm -f parse.tab.h
	rm -f *.output
	rm -f *.o
	rm -f *~

$(FLEX_O): $(FLEX_C) $(BISON_H)
$(BISON_O): $(BISON_C) $(BISON_H)

