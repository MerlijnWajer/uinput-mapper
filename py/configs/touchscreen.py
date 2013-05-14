from cinput import *

# Approx

# top left: (300, 3500)
# bottom left: 300, 300)

# top right: (3000, 3700)
# bottom right: (3880, 430)

w = 1920.
h = 1080.

rx1 = 300.
ry1 = 200.

rx2 = 3800.
ry2 = 4000.

def transform_x(x):
    x -= rx1
    x *= w / (rx2 - rx1)

    return int(x)

def transform_y(y):
    y = ry2 - y
    y -= ry1
    y *= h / (rx2 - rx1)

    return int(y)

config = {
        EV_ABS : {
            ABS_X : {
                'type' : EV_ABS,
                'code' : ABS_X,
                'value' : transform_x
            },
            ABS_Y : {
                'type' : EV_ABS,
                'code' : ABS_Y,
                'value' : transform_y
            }
        }
}

def config_merge(c):
    # XXX: We cannot just use update; as it will override everything in say EV_KEY
    for k, v in config.iteritems():
        if k in c:
            c[k].update(v)
        else:
            c[k] = v

    # Uncomment this to make touch click too
    c[EV_KEY][BTN_TOUCH] = {
            'type' : EV_KEY,
            'code' : BTN_TOUCH,
            'value' : lambda x: 0
    }


