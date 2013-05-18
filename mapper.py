# encoding: utf-8
import cinput

# XXX: Also parse name, etc
def parse_conf(f, devname):
    conf = {}
    e = f.get_exposed_events()
    for k, v in e.iteritems():
        t = cinput.events[k]
        if t == cinput.EV_SYN:
            continue

        conf[(devname, t)] = {}

        for key in v:
            tt = cinput.event_keys[t][key]
            conf[(devname, t)][tt] = {
                'type' : (devname, t),
                'code' : tt,
                'value' : None
                #'value' : lambda x: x
            }

    return conf


def pretty_conf_print(c):
    for k, v in c.iteritems():
        print 'Input:', k[0], 'Type:', cinput.rev_events[k[1]]
        for kk, vv in v.iteritems():
            n_ev_d, n_ev_t = vv['type']
            print ' ' * 4,
            print cinput.rev_event_keys[k[1]][kk],
            print ' → ([%d, %s], %s)' % (n_ev_d,
                cinput.rev_events[n_ev_t],
                cinput.rev_event_keys[n_ev_t][vv['code']])


class KeyMapper(object):
    def __init__(self, config):
        self._config = config

    def map_event(self, ev):
        _type = ev.type
        if _type in self._config:
            typemaps = self._config[_type]
            if ev.code in typemaps:
                info = typemaps[ev.code]
                ev.type = info['type']
                ev.code = info['code']
                if info['value'] is not None:
                    ev.value = info['value'](ev.value)
                else:
                    ev.value = ev.value

        return ev

    def expose(self, d):
        for evt, v in self._config.iteritems():
            for code, dat in v.iteritems():
                d.expose_event_type(dat['type'])
                d.expose_event(dat['type'], dat['code'])
