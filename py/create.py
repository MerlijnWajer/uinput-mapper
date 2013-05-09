import linux_uinput, ctypes, fcntl, os, sys
from cinput import *
from mapper import KeyMapper, parse_conf
from example_conf import config
from linux_input import timeval, input_event


try:
    import cPickle as pickle
except ImportError:
    import pickle

f = pickle.Unpickler(sys.stdin)

conf = f.load()
m = KeyMapper(conf)

d = UInputDevice()
m.expose(d)
d.setup('Example input device')


while True:
    ev = f.load()
    # Use code below rather than the line above if you use an old python
    # version (also edit read.py)

    #ev_p = f.load()
    #ti = timeval(ev_p[0], ev_p[1])
    #ev = input_event(ti, ev_p[2], ev_p[3], ev_p[4])

    ev = m.map_event(ev)

    d.fire_event(ev)

    #try:
    #    print ev.time.tv_sec, ev.time.tv_usec
    #    s = '%s %s %d' % (rev_events[ev.type], rev_event_keys[ev.type][ev.code], ev.value)
    #    print 'Event type:', s

    #except KeyError:
    #   pass
