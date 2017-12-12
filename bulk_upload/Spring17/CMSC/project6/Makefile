CC = gcc
CFLAGS = -g -ansi -pedantic-errors -Wall -Werror -Wshadow -Wwrite-strings

all:	d8sh.o executor.o parser.tab.o lexer.o
		$(CC) d8sh.o executor.o parser.tab.o lexer.o -lreadline -o d8sh

clean:
		rm -f *.o *.x *~ d8sh

lexer.o:	lexer.h parser.tab.h lexer.c
		$(CC) $(CFLAGS) -c lexer.c

parser.tab.o: command.h parser.tab.h parser.tab.c
		$(CC) $(CFLAG) -c parser.tab.c

executor.o:	command.h executor.h executor.c
		$(CC) $(CFLAGS) -c executor.c

d8sh.o:	lexer.h executor.h d8sh.c
		$(CC) $(CFLAGS) -c	lexer.c executor.c d8sh.c

d8sh:	d8sh.o executor.o parser.tab.o lexer.o
		$(CC) d8sh.o executor.o parser.tab.o lexer.o -lreadline -o d8sh
