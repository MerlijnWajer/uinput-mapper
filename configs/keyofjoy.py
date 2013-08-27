from uinputmapper.cinput import *


"""
"""

# Fake repeats (will set to 2)
repete = 0

# Threshold before sending event
threshold = 42

def squash_gen(neg, pos):
    pkey = [None, 0]

    def squash(ev):
        if ev.value > threshold:
            ev.code = neg
            pkey[0] = neg

            ev.value = 1 + (pkey[1] & repete)
            pkey[1] = 1
        elif ev.value < -threshold:
            ev.code = pos
            pkey[0] = pos

            ev.value = 1 + (pkey[1] & repete)
            pkey[1] = 1
        else:
            if pkey[0] is None:
                ev.type = EV_SYN
                ev.code = SYN_REPORT
                ev.value = 0
            else:
                ev.code = pkey[0]
                ev.value = 0
                pkey[1] = 0
                pkey[0] = None

    return squash


config = {
        (0, EV_KEY): {
            BTN_X: {
                'type' : (0, EV_KEY),
                'code' : KEY_X,
                'value' : None
            },
            BTN_Y: {
                'type' : (0, EV_KEY),
                'code' : KEY_Y,
                'value' : None
            },
            BTN_Z: {
                'type' : (0, EV_KEY),
                'code' : KEY_Z,
                'value' : None
            },
            BTN_A: {
                'type' : (0, EV_KEY),
                'code' : KEY_A,
                'value' : None
            },
            BTN_B: {
                'type' : (0, EV_KEY),
                'code' : KEY_B,
                'value' : None
            },
            BTN_C: {
                'type' : (0, EV_KEY),
                'code' : KEY_C,
                'value' : None
            },
            BTN_TR: {
                'type' : (0, EV_KEY),
                'code' : KEY_R,
                'value' : None
            },
            BTN_TL: {
                'type' : (0, EV_KEY),
                'code' : KEY_L,
                'value' : None
            },
            BTN_TL2: {
                'type' : (0, EV_KEY),
                'code' : KEY_BACKSPACE,
                'value' : None
            }
        },
        (0, EV_ABS) : {
            ABS_Y : {
                'type' : (0, EV_KEY),
                'code' : KEY_UP,
                'func' : squash_gen(KEY_DOWN, KEY_UP)
            },
            ABS_X : {
                'type' : (0, EV_KEY),
                'code' : KEY_LEFT,
                'func' : squash_gen(KEY_RIGHT, KEY_LEFT)
            },
            ABS_WHEEL : {
                'type' : (0, EV_KEY),
                'code' : KEY_DOWN,
                'value' : None
            },
            ABS_BRAKE : {
                'type' : (0, EV_KEY),
                'code' : KEY_RIGHT,
                'value' : None
            }
        }
}

def config_merge(c):
    c.clear()
    c.update(config)
