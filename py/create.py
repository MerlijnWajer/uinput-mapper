import cinput, linux_uinput, ctypes, fcntl, os


from cinput import *

def handle_specs(f, s):
    print 'ioctl:', fcntl.ioctl(f, UI_SET_EVBIT, cinput.EV_KEY)
    print 'ioctl:', fcntl.ioctl(f, UI_SET_KEYBIT, cinput.KEY_UP)


d = cinput.UInputDevice('Example input device', None)

import time
time.sleep(5)


# Config
dev = {
   "input_devices" : [
        ("/dev/input/event3", "keyboard1"),
   ],
   "type" : "mouse", # "mixed" "mouse" "keyboard" "joystick" "clone"?
   "keymap" : {
       "any" : { # From
           EV_KEY : {
               KEY_UP : {
                    "type" : EV_REL,
                    "key" : REL_X,
                    "value" : lambda x: -x*10
               },
               KEY_DOWN : {
                    "type": EV_REL,
                    "key": REL_X,
                    "value" : lambda x: x*10
               }
           }
       },
   }
}
