import cinput
import ctypes

import sys

f = open(sys.argv[1] if len(sys.argv) == 2 else "/dev/input/event3")

print 'Version:', cinput.get_input_version(f)
print cinput.get_input_name(f)
print cinput.EVIOCGBIT(0, cinput.EV_MAX)

import struct, array, fcntl

bpl = struct.calcsize('@L') * 8
nbits = lambda x: ((x-1) / bpl) + 1

ll = nbits(cinput.KEY_MAX)

test_bit = lambda j, v: (v[j / bpl] >> (j % bpl)) & 1

#for b in xrange(cinput.EV_MAX):
for b in xrange(1, 2):

    buf = array.array('L', [0L] * ll)
    print 'ioctl return:', fcntl.ioctl(f, cinput.EVIOCGBIT(b, cinput.KEY_MAX), buf)
    v = struct.unpack('@%dL' % ll, buf)
    print v

    for j in range(0, cinput.KEY_MAX):
        if test_bit(j, v):
            print cinput.rev_keys[j]


    del buf

while True:
    estr = f.read(ctypes.sizeof(cinput.input_event))

    e = ctypes.cast(estr, ctypes.POINTER(cinput.input_event))
    ev = e.contents

    print 'Event type:', cinput.rev_events[ev.type]
    try:
        print 'Code:', cinput.event_keys[ev.type][ev.code]
    except KeyError:
       pass
