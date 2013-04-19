from linux_input import *
from linux_uinput import *

import array, struct, fcntl, os

def get_input_version(f):
    """
    Returns the input version of a specified fd of a device
    """
    buf = array.array('i', [0])
    r = fcntl.ioctl(f, EVIOCGVERSION, buf)
    v = struct.unpack('@i', buf)[0]
    del r
    return "%d.%d.%d" % ( v >> 16, (v >> 8) & 0xff, v & 0xff)

def get_input_name(f, l=256):
    """
    Returns the name of a specified fd of a device
    """
    buf = array.array('c', ' ' * l)
    r = fcntl.ioctl(f, EVIOCGNAME(l), buf)
    v = struct.unpack('%ds' % l, buf)
    del r
    return v

_bpl = struct.calcsize('@L') * 8
_nbits = lambda x: ((x-1) / _bpl) + 1
_ll = _nbits(KEY_MAX)
test_bit = lambda j, v: (v[j / _bpl] >> (j % _bpl)) & 1

# TODO: Do this for all EV_* ?
def get_keys(f, ev):
    buf = array.array('L', [0L] * _ll)
    try:
        fcntl.ioctl(f, EVIOCGBIT(ev, KEY_MAX), buf)
    except IOError:
        print 'Whoops!'
        yield None
        return

    v = struct.unpack('@%dL' % _ll, buf)
    del buf

    for j in range(0, KEY_MAX):
        if test_bit(j, v):
            yield j

    return


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

def create_uinput_device(name, specs):
    """
    Create uinput device
    """
    f = open_uinput()

    if not f:
        print 'Failed to open uinput'
        return None

    # Add keys, etc
    #handle_specs(f, specs)

    # Allocate other info
    uidev = uinput_user_dev()

    # TODO: Get from specs
    uidev.name = name
    uidev._id.bustype = 0x03 # BUS_USB (TODO)
    uidev._id.vendor = 0x42
    uidev._id.product = 0xbebe
    uidev._id.version = 1

    buf = buffer(uidev)[:]

    # Write dev info
    os.write(f, buf)

    fcntl.ioctl(f, UI_DEV_CREATE)

    return f

def free_uinput_device(f):
    return fcntl.ioctl(f, UI_DEV_DESTROY)

class UInputDevice(object):

    def __init__(self, name, specs):
        self.f = create_uinput_device(name, specs)

    def __del__(self):
        free_uinput_device(self.f)

