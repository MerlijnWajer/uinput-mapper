import cinput
import ctypes

import sys

print sys.argv[1]
f = open(sys.argv[1] if len(sys.argv) else "/dev/input/event8")

while True:
    estr = f.read(ctypes.sizeof(cinput.input_event))

    e = ctypes.cast(estr, ctypes.POINTER(cinput.input_event))
    ev = e.contents

    if ev.type == cinput.EV_KEY:
        print cinput.rev_keys[ev.code]
    if ev.type == cinput.EV_REL:
        print cinput.rev_rel[ev.code]
    if ev.type == cinput.EV_ABS:
        print cinput.rev_absaxes[ev.code]
    if ev.type == cinput.EV_SYN:
        print cinput.rev_syn[ev.code]

    #print e.contents.type
    #print e.contents.code
    #print e.contents.value

