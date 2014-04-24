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
        },
        KEY_SPACE : {
            'type' : (0, EV_KEY),
            'code' : KEY_SPACE,
            'value' : None
        },
        KEY_C : {
            'type' : (0, EV_KEY),
            'code' : KEY_C,
            'value' : None
        },
        KEY_LEFTCTRL : {
            'type' : (0, EV_KEY),
            'code' : KEY_LEFTCTRL,
            'value' : None
        },
    }
}

names = {
    0 : 'Example a-b keyboard'
}

# Export extra keys. In our case: export KEY_B with type EV_KEY ; to ofd 0.
# We need to add it here, because it isn't export in our config dictionary; but
# it can be returned from the keyswap function. (and uinput wants to know what
# keys are exported at creation time)
extra_key_exports = [
    (0, EV_KEY, KEY_B),
]

def config_merge(c, n):
    c.clear()
    n.update(names)
    for k, v in config.iteritems():
        if k in c:
            c[k].update(v)
        else:
            c[k] = v
