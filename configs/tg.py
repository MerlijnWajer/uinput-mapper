from uinputmapper.cinput import *

config = {
        (0, EV_KEY) : {
            BTN_MIDDLE : {
                'type' : (0, EV_KEY),
                'code' : KEY_RIGHTMETA,
                'value' : None
            }
        }
}

def config_merge(c):
    c.clear()
    c.update(config)
