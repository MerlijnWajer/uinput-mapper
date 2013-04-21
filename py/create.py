import linux_uinput, ctypes, fcntl, os, sys

from cinput import *

from mapper import KeyMapper, parse_conf


from example_conf import config

clone = False

f = InputDevice(sys.argv[1] if len(sys.argv) == 2 else "/dev/input/event3")
d = UInputDevice()

if clone:
    conf = parse_conf(f)
    m = KeyMapper(conf)

else:
    m = KeyMapper(config)

m.expose(d)

d.setup('Example input device' )


while True:
    ev = f.next_event()

    ev = m.map_event(ev)

    d.fire_event(ev)

    #try:
    #    print ev.time.tv_sec, ev.time.tv_usec
    #    s = '%s %s %d' % (rev_events[ev.type], rev_event_keys[ev.type][ev.code], ev.value)
    #    print 'Event type:', s

    #except KeyError:
    #   pass
