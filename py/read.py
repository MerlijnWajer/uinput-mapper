import linux_uinput, ctypes, fcntl, os, sys
from cinput import *
from mapper import KeyMapper, parse_conf
from example_conf import config

clone = True

f = InputDevice(sys.argv[1] if len(sys.argv) == 2 else "/dev/input/event3")

if clone:
    config = parse_conf(f)
    m = KeyMapper(config)
else:
    m = KeyMapper(config)

try:
    import cPickle as pickle
except ImportError:
    import pickle
p = pickle.Pickler(sys.stdout)

p.dump(config)
sys.stdout.flush()

#d = UInputDevice()
#m.expose(d)
#d.setup('Example input device')


while True:
    ev = f.next_event()
    p.dump(ev)

    # Use this rather than the line above if you use an old python version (also
    # edit create.py)
    #p.dump((ev.time.tv_sec, ev.time.tv_usec, ev.type, ev.code, ev.value))

    sys.stdout.flush()

    #ev = m.map_event(ev)

    #d.fire_event(ev)

    #try:
    #    print ev.time.tv_sec, ev.time.tv_usec
    #    s = '%s %s %d' % (rev_events[ev.type], rev_event_keys[ev.type][ev.code], ev.value)
    #    print 'Event type:', s

    #except KeyError:
    #   pass
