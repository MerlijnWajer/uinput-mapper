from cinput import *

def transform_x(x):
    print 'old y', x

    # offset
    x -= 200

    x = int(x / (3800. / 1366.))
    #x = int(x / (3800. / 1920.))
    print 'new x', x
    return x

def transform_y(y):
   print 'old y', y

   # invert
   y = 3800 - y

   # offset
   y -= 200
   y = int(y / (3800. / 768.))
   #y = int(y / (3800. / 1080.))
   print 'new y', y
   return y

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
