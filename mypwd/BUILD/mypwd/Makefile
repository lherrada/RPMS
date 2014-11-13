GCC=gcc
CFLAGS=-c -Wall
CP=cp
INSTALL_BIN=/bin/
all: mypwd


mypwd: getcwd.o pwd.o getcwd.h 
	$(GCC) -Wall -o $@ $^

getcwd.o: getcwd.c 
	$(GCC) -o $@ $< $(CFLAGS)

pwd.o: pwd.c
	$(GCC) $(CFLAGS) $< 

install:
	$(CP) mypwd $(INSTALL_BIN) 

clean:
	rm -f *.o mypwd

