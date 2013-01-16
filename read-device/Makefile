.PHONY: default clean

CFLAGS+=-ansi -pedantic -Wall -Wextra -Werror -Wno-unused-result
CFLAGS+=-pipe -O2
CFLAGS+=-D_BSD_SOURCE

default: read

map: read.c
	$(CC) read.c $(CFLAGS) -o read

clean:
	rm -f read
