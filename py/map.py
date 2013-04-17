import cinput
import ctypes

import sys

f = open(sys.argv[1] if len(sys.argv) == 2 else "/dev/input/event8")

while True:
    estr = f.read(ctypes.sizeof(cinput.input_event))

    e = ctypes.cast(estr, ctypes.POINTER(cinput.input_event))
    ev = e.contents

    print 'Event type:', cinput.rev_events[ev.type]
    try:
        print 'Code:', cinput.event_keys[ev.type][ev.code]
    except KeyError:
        pass
