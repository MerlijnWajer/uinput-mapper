.PHONY: default clean

PREFIX=/usr/local
CFLAGS+=-ansi -pedantic -pipe -D_BSD_SOURCE \
	-Wall -Wextra -Werror -Wno-unused-result
OPT=-O2

all: map

debug: OPT=-O0
debug: CFLAGS+=-ggdb
debug: map

def_keys.h:
	echo '#include <linux/input.h>' | gcc -E -dM - \
	| grep '#define KEY_' | cut -f2 -d" " | sed 's/KEY_.*/DEF_KEY(&)/' \
	> $@

map: map.c def_keys.h config.h config_functions.h
	$(CC) $(CFLAGS) ${OPT} map.c -o $@

clean:
	rm -f map def_keys.h

install:
	install map ${PREFIX}/sbin/uinput-mapper
