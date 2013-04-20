from cinput import *
import ctypes

import sys

#f = open(sys.argv[1] if len(sys.argv) == 2 else "/dev/input/event3")
f = InputDevice(sys.argv[1] if len(sys.argv) == 2 else "/dev/input/event3")

print 'Version:', f.get_version()
print f.get_name()

d = f.get_exposed_events()
for k, v in d.iteritems():
    print k + ':', ', '.join(v)

while True:
    ev = f.next_event()

    try:
        print ev.time.tv_sec, ev.time.tv_usec
        s = '%s %s %d' % (rev_events[ev.type], rev_event_keys[ev.type][ev.code], ev.value)
        print 'Event type:', s
    except KeyError:
       pass
