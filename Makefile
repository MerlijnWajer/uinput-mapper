.PHONY: default clean

CFLAGS+=-ansi -pedantic -Wall -Wextra -Werror -Wno-unused-result
CFLAGS+=-pipe -O2
CFLAGS+=-D_BSD_SOURCE

default: map

def_keys.h:
	echo '#include <linux/input.h>' | gcc -E -dM - | grep '#define KEY_' | cut -f2 -d" " | sed 's/KEY_.*/DEF_KEY(&)/' > def_keys.h

def_buttons.h:
	echo '#include <linux/input.h>' | gcc -E -dM - | grep '#define BTN_' | cut -f2 -d" " | sed 's/BTN_.*/DEF_BTN(&)/' > def_buttons.h

map: map.c def_keys.h def_buttons.h config.h config_functions.h
	$(CC) map.c $(CFLAGS) -o map

all: map
	mv config.h config.bak
	for file in confs/*.h; \
	do \
	echo $$file; \
	cp $$file config.h; \
	$(CC) map.c $(CFLAGS) -o map$$(echo $$file | sed 's/confs\//_/;s/\.h//' ); \
	done
	mv config.bak config.h

clean:
	rm -f map def_keys.h map_*
