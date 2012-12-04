.PHONY: default clean

CFLAGS+=-ansi -pedantic -Wall -Wextra -Werror -Wno-unused-result
CFLAGS+=-pipe -O2
CFLAGS+=-D_BSD_SOURCE

default: map

keys:
	echo '#include <linux/input.h>' | gcc -E -dM - | grep '#define KEY_' | cut -f2 -d" " | sed 's/KEY_.*/DEF_KEY(&)/' > def_keys.h

map: map.c keys
	$(CC) map.c $(CFLAGS) -o map

clean:
	rm -f map def_keys.h
