echo '#include <linux/input.h>' | gcc -E -dM - | grep '#define KEY_' | cut -f2 -d" " | sed 's/KEY_.*/DEF_KEY(&)/' > def_keys.h
