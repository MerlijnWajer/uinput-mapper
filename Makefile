.PHONY: default clean

CFLAGS+=-ansi -pedantic -Wall -Wextra -Werror -Wno-unused-result
CFLAGS+=-pipe -O2
CFLAGS+=-D_BSD_SOURCE

default: map

keys:
	bash genkeys.sh

map: map.c keys
	$(CC) map.c $(CFLAGS) -o map

clean:
	rm -f map def_keys.h
