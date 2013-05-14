from cinput import *

overrule = lambda x: -x*2
passthrough = lambda x: x

config = {
        EV_REL : {
            #REL_X : {
            #    'type' : EV_REL,
            #    'code' : REL_X,
            #    'value': overrule
            #},
            #REL_Y : {
            #    'type': EV_REL,
            #    'code': REL_Y,
            #    'value' : overrule
            #},
            REL_X : {
                'type' : EV_REL,
                'code' : REL_X,
                'value' : lambda x: 0
            },
            REL_Y : {
                'type' : EV_REL,
                'code' : REL_Y,
                'value' : lambda x: 0
            },
            REL_WHEEL : {
                'type' : EV_REL,
                'code' : REL_WHEEL,
                'value' : lambda x: -x*2
            }
        },
        EV_KEY : {
            BTN_LEFT : {
                'type' : EV_KEY,
                'code' : BTN_LEFT,
                'value' : passthrough
            }
        }
}

def config_merge(c):
    for k, v in config.iteritems():
        if k in c:
            c[k].update(v)
        else:
            c[k] = v
