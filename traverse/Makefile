TARGET	= traverse
OBJS	= traverse.o 

CC		= g++
CFLAGS		= -O2
CXXFLAGS 	+= -fpermissive 
CXXFLAGS 	+= -std=c++11
LDFLAGS		= 
INCLUDES	= -I./
LIBS		= -lm -lpthread -ltbb

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(LDFLAGS) -o $@ $(OBJS) $(LIBS) 

$(OBJS): timer.h 

.c.o:
	$(CC) $(CFLAGS) $(CXXFLAGS) $(INCLUDES) -c $< 

clean:
	rm -rf $(TARGET) $(OBJS) *~

