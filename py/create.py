import linux_uinput, ctypes, fcntl, os, sys

from cinput import *

clone = True

overrule = lambda x: -x*2
passthrough = lambda x: x
config = {
        EV_REL : {
            REL_X : {
                'type' : EV_REL,
                'code' : REL_X,
                'value': overrule
            },
            REL_Y : {
                'type': EV_REL,
                'code': REL_Y,
                'value' : overrule
            }
        },
        EV_KEY : {
            BTN_LEFT : {
                'type' : EV_KEY,
                'code' : BTN_LEFT,
                'value' : passthrough
            }
        }
}


f = InputDevice(sys.argv[1] if len(sys.argv) == 2 else "/dev/input/event3")

d = UInputDevice()


if clone:
    e = f.get_exposed_events()
    for k, v in e.iteritems():
        t = events[k]
        if t == EV_SYN:
            continue
        d.expose_event_type(t)
        for key in v:
            tt = event_keys[t][key]
            d.expose_event(t, tt)

        print k + ':', ', '.join(v)
else:
    for evt, v in config.iteritems():
        for code, dat in v.iteritems():
            d.expose_event_type(dat['type'])
            d.expose_event(dat['type'], dat['code'])


d.setup('Example input device' )


def map_ev(ev):

    _type = ev.type
    if _type in config:
        typemaps = config[_type]
        if ev.code in typemaps:
            info = typemaps[ev.code]
            ev.type = info['type']
            ev.code = info['code']
            ev.value = info['value'](ev.value)

    return ev

while True:
    ev = f.next_event()

    if not clone:
        ev = map_ev(ev)

    d.fire_event(ev)

    try:
        #print ev.time.tv_sec, ev.time.tv_usec
        s = '%s %s %d' % (rev_events[ev.type], rev_event_keys[ev.type][ev.code], ev.value)
        print 'Event type:', s

    except KeyError:
       pass
