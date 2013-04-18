import ctypes

"""
struct input_event {
    struct timeval time;
    __u16 type;
    __u16 code;
    __s32 value;
};
"""

class timeval(ctypes.Structure):
    _fields_ = [("tv_sec", ctypes.c_long), ("tv_usec", ctypes.c_long)]

class input_event(ctypes.Structure):
    _fields_ = [
        ("time", timeval),
        ("type", ctypes.c_uint16),
        ("code", ctypes.c_uint16),
        ("value", ctypes.c_int32)
    ]

from ioctlhelp import IOR, IOW, IOC, IO, _IOC_READ

# Get driver version
EVIOCGVERSION = IOR(ord('E'), 0x01, '@i')

# Get device ID
#EVIOCGID = IOR(ord('E'), 0x02, struct input_id)

# Get repeat settings
EVIOCGREP = IOR(ord('E'), 0x03, '@ii')
# Set repeat settings
EVIOCSREP = IOW(ord('E'), 0x03, '@ii')

# Get keycode
EVIOCGKEYCODE = IOR(ord('E'), 0x04, '@ii')
# EVIOCGKEYCODE_V2 _IOR('E', 0x04, struct input_keymap_entry)

# Set keycode

EVIOCSKEYCODE = IOW(ord('E'), 0x04, '@ii')
#EVIOCSKEYCODE_V2 _IOW('E', 0x04, struct input_keymap_entry)

# Get device name
EVIOCGNAME = lambda _len: IOC(_IOC_READ, ord('E'), 0x06,
        struct.calcsize('%ds' % _len))

# Get physical location
EVIOCGPHYS= lambda _len: IOC(_IOC_READ, ord('E'), 0x07,
        struct.calcsize('%ds' % _len))

# Get unique identifier
EVIOCGUNIQ = lambda _len: IOC(_IOC_READ, ord('E'), 0x08,
        struct.calcsize('%ds' % _len))

# Get device properties
EVIOCGPROP = lambda _len: IOC(_IOC_READ, ord('E'), 0x09,
        struct.calcsize('%ds' % _len))

#EVIOCGMTSLOTS(len)	_IOC(_IOC_READ, 'E', 0x0a, len)
#
#EVIOCGKEY(len)		_IOC(_IOC_READ, 'E', 0x18, len)		/* get global key state */
#EVIOCGLED(len)		_IOC(_IOC_READ, 'E', 0x19, len)		/* get all LEDs */
#EVIOCGSND(len)		_IOC(_IOC_READ, 'E', 0x1a, len)		/* get all sounds status */
#EVIOCGSW(len)		_IOC(_IOC_READ, 'E', 0x1b, len)		/* get all switch states */


# Get event bits
EVIOCGBIT = lambda ev, _len: IOC(_IOC_READ, ord('E'), 0x20 + ev, _len)

#EVIOCGABS(abs)		_IOR('E', 0x40 + (abs), struct input_absinfo)	/* get abs value/limits */
#EVIOCSABS(abs)		_IOW('E', 0xc0 + (abs), struct input_absinfo)	/* set abs value/limits */
#
#EVIOCSFF		_IOC(_IOC_WRITE, 'E', 0x80, sizeof(struct ff_effect))	/* send a force effect to a force feedback device */
#EVIOCRMFF		_IOW('E', 0x81, int)			/* Erase a force effect */
#EVIOCGEFFECTS		_IOR('E', 0x84, int)			/* Report number of effects playable at the same time */
#
#EVIOCGRAB		_IOW('E', 0x90, int)			/* Grab/Release device */
#
#EVIOCSCLOCKID		_IOW('E', 0xa0, int)			/* Set clockid to be used for timestamps */

import array, struct, fcntl

def get_input_version(f):
    buf = array.array('i', [0])
    r = fcntl.ioctl(f, EVIOCGVERSION, buf)
    v = struct.unpack('@i', buf)[0]
    del r
    return "%d.%d.%d" % ( v >> 16, (v >> 8) & 0xff, v & 0xff)

def get_input_name(f, l=256):
    buf = array.array('c', ' ' * l)
    r = fcntl.ioctl(f, EVIOCGNAME(l), buf)
    v = struct.unpack('%ds' % l, buf)
    del r
    return v
