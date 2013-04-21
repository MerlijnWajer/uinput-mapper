import cinput

def parse_conf(f):
    conf = {}
    e = f.get_exposed_events()
    for k, v in e.iteritems():
        t = cinput.events[k]
        if t == cinput.EV_SYN:
            continue

        conf[t] = {}

        for key in v:
            tt = cinput.event_keys[t][key]
            conf[t][tt] = {
                'type' : t,
                'code' : tt,
                'value' : lambda x: x
            }

    return conf

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
                ev.value = info['value'](ev.value)

        return ev

    def expose(self, d):
        for evt, v in self._config.iteritems():
            for code, dat in v.iteritems():
                d.expose_event_type(dat['type'])
                d.expose_event(dat['type'], dat['code'])
