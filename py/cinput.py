from linux_input import *
from linux_uinput import *

import array, struct, fcntl, os, sys

def get_input_version(f):
    """
    Returns the input version of a specified fd of a device
    """
    buf = array.array('i', [0])
    r = fcntl.ioctl(f, EVIOCGVERSION, buf)
    v = struct.unpack('@i', buf)[0]
    del buf
    return "%d.%d.%d" % ( v >> 16, (v >> 8) & 0xff, v & 0xff)

def get_input_name(f, l=256):
    """
    Returns the name of a specified fd of a device
    """
    buf = array.array('c', ' ' * l)
    r = fcntl.ioctl(f, EVIOCGNAME(l), buf)
    v = struct.unpack('%ds' % l, buf)[0]
    del buf
    return v[:r]

_bpl = struct.calcsize('@L') * 8
_nbits = lambda x: ((x-1) / _bpl) + 1
_ll = _nbits(KEY_MAX)
test_bit = lambda j, v: (v[j / _bpl] >> (j % _bpl)) & 1

def get_keys(f, ev):
    buf = array.array('L', [0L] * _ll)
    try:
        fcntl.ioctl(f, EVIOCGBIT(ev, KEY_MAX), buf)
    except IOError:
        #print >>sys.stderr, 'Whoops!', rev_events[ev]
        return None

    v = struct.unpack('@%dL' % _ll, buf)
    del buf

    r = []
    for j in range(0, KEY_MAX):
        if test_bit(j, v):
            r.append(j)

    return r


def copy_event(estr):
    e = ctypes.cast(estr, ctypes.POINTER(input_event))
    ev = e.contents

    return input_event(ev.time, ev.type, ev.code, ev.value)

class InputDevice(object):

    def __init__(self, path):
        self._f = open(path)

    def get_version(self):
        return get_input_version(self._f)

    def get_name(self):
        return get_input_name(self._f)

    def get_exposed_events(self):
        d = dict()
        for k, v in events.iteritems():
            l = get_keys(self._f, v)
            if l:
                d[k] = []
                for ev in l:
                    try:
                        d[k].append(event_keys[v][ev])
                    except KeyError:
                        pass

        return d

    def next_event(self):
        estr = self._f.read(ctypes.sizeof(input_event))
        return copy_event(estr)

    def get_fd(self):
        return fd


    def __del__(self):
        self._f.close()


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

def write_uinput_device_info(name):
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
        # TODO: Other methods for specs etc
        # TODO: Maybe don't create the device yet; add a seperate method?
        # TODO: Take inspiration from the config.h files ! Also allow using
        # direct methods / programming it rather than just the dict as config
        self._f = write_uinput_device_info(name)

    def __del__(self):
        free_uinput_device(self._f)

