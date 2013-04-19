import cinput, linux_uinput, ctypes, fcntl, os


def open_uinput():
    try:
        f = os.open('/dev/uinput',  os.O_WRONLY | os.O_NONBLOCK)
    except IOError:
        try:
            f = os.open('/dev/input/uinput', os.O_WRONLY | os.O_NONBLOCK)
        except IOError:
            print 'FAIL MUCH?'
            return None
    return f

def handle_specs(f, s):
    print 'ioctl:', fcntl.ioctl(f, linux_uinput.UI_SET_EVBIT, cinput.EV_KEY)
    print 'ioctl:', fcntl.ioctl(f, linux_uinput.UI_SET_KEYBIT, cinput.KEY_UP)


def create_device(specs):
    f = open_uinput()

    if not f:
        print 'Failed to open uinput'
        return None

    # Add keys, etc
    handle_specs(f, specs)

    # Allocate other info
    uidev = linux_uinput.uinput_user_dev()

    uidev.name = 'key2joy:0'
    uidev._id.bustype = 0x03 # BUS_USB (TODO)
    uidev._id.vendor = 0x42
    uidev._id.product = 0xbebe
    uidev._id.version = 1

    buf = buffer(uidev)[:]

    # Write dev info
    os.write(f, buf)

    print 'ioctl:', fcntl.ioctl(f, linux_uinput.UI_DEV_CREATE)

    return f

def free_device(f):
    return fcntl.ioctl(f, linux_uinput.UI_DEV_DESTROY)


_ = create_device(None)

print 'Hoi'
import time
time.sleep(5)

free_device(_)
# config
#dev = {
#   "input_devices" : [
#        ("/dev/input/event3", "keyboard1"),
#   ],
#   "type" : "mouse", # "mixed" "mouse" "keyboard" "joystick" "clone"?
#   "keymap" : {
#       "any" : { # From
#           EV_KEY : {
#               KEY_UP : {
#                    "type" : EV_REL
#                    "key" : REL_X
#                    "value" : lambda x: -x*10
#               }
#               KEY_DOWN : {
#                    "type": EV_REL
#                    "key": REL_X
#                    "value" : lambda x: x*10
#               }
#           }
#       },
#   }
#}
