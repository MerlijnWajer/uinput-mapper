import cinput
import ctypes

import sys

f = open(sys.argv[1] if len(sys.argv) == 2 else "/dev/input/event3")

print 'Version:', cinput.get_input_version(f)
print cinput.get_input_name(f)

print [cinput.rev_keys[_] for _ in cinput.get_keys(f, cinput.EV_KEY)]
print [cinput.rev_absaxes[_] for _ in cinput.get_keys(f, cinput.EV_ABS)]
print [cinput.rev_rel[_] for _ in cinput.get_keys(f, cinput.EV_REL)]

while True:
    estr = f.read(ctypes.sizeof(cinput.input_event))

    e = ctypes.cast(estr, ctypes.POINTER(cinput.input_event))
    ev = e.contents

    print 'Event type:', cinput.rev_events[ev.type]
    try:
        print 'Code:', cinput.event_keys[ev.type][ev.code]
    except KeyError:
       pass
