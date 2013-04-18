from linux_input import *

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

_bpl = struct.calcsize('@L') * 8
_nbits = lambda x: ((x-1) / _bpl) + 1
_ll = _nbits(KEY_MAX)
test_bit = lambda j, v: (v[j / _bpl] >> (j % _bpl)) & 1

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
            #yield rev_keys[j]

    return

