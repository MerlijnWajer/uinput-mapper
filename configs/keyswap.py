from uinputmapper.cinput import *


"""
This example configuration takes a keyboard as input (or: anything that exports
KEY_A and will alternate the KEY_A with KEY_B. This shows of the simple "func"
key in the config.

"""

key_toggle = 0

def keyswap(ev):
    global key_toggle
    if ev.value == 1:
        key_toggle = not key_toggle

    ev.code = KEY_A if key_toggle else KEY_B
    ev.type = EV_KEY
    ev.value = ev.value # Effectively a NOP, not required

    return ev

config = {
    (0, EV_KEY) : {
        KEY_A : {
            'type' : (0, EV_KEY),
            'code' : KEY_A,
            'func' : keyswap
        }
    }
}

names = {
    0 : 'Example a-b keyboard'
}

extra_exports = [
# TODO
]

def config_merge(c, n):
    n.update(names)
    for k, v in config.iteritems():
        if k in c:
            c[k].update(v)
        else:
            c[k] = v
