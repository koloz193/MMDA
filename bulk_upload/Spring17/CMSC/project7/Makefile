# Name: Zachary Kolodny
# UID #: 112311827
# UID: zkolodny

CC = gcc
CFLAGS = -c -g -ansi -pedantic-errors -Wall -Werror -Wshadow -Wwrite-strings

all:
	make public01 public02 public03 public04

clean:
	rm -f *.o public01 public02 public03 public04 tester *~

bag.o: bag.h bag.c bag-implementation.h
	$(CC) $(CFLAGS) bag.c

my_memory_checker_216.o: my_memory_checker_216.c my_memory_checker_216.h
	$(CC) $(CFLAGS) my_memory_checker_216.c

tester.o: tester.c bag.h
	$(CC) $(CFLAGS) tester.c

public01.o: public01.c bag.h
	$(CC) $(CFLAGS) public01.c

public02.o: public02.c bag.h
	$(CC) $(CFLAGS) public02.c

public03.o: public03.c bag.h
	$(CC) $(CFLAGS) public03.c

public04.o: public04.c bag.h my_memory_checker_216.h
	$(CC) $(CFLAGS) public04.c

public01: public01.o bag.o
	$(CC) public01.o bag.o -o public01

public02: public02.o bag.o
	$(CC) public02.o bag.o -o public02

public03: public03.o bag.o
	$(CC) public03.o bag.o -o public03

public04: public04.o bag.o my_memory_checker_216.o
	$(CC) public04.o bag.o my_memory_checker_216.o -o public04

tester: tester.o bag.o
	$(CC) tester.o bag.o -o tester
