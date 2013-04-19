from cinput import *
import ctypes

import sys

f = open(sys.argv[1] if len(sys.argv) == 2 else "/dev/input/event3")

print 'Version:', get_input_version(f)
print get_input_name(f)

print [rev_keys[_] for _ in get_keys(f, EV_KEY)]
print [rev_absaxes[_] for _ in get_keys(f, EV_ABS)]
print [rev_rel[_] for _ in get_keys(f, EV_REL)]

while True:
    estr = f.read(ctypes.sizeof(input_event))

    e = ctypes.cast(estr, ctypes.POINTER(input_event))
    ev = e.contents

    print 'Event type:', rev_events[ev.type]
    try:
        print 'Code:', event_keys[ev.type][ev.code]
    except KeyError:
       pass
