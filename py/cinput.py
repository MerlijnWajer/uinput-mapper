import cinput

from gen import input_constants_dict

for k, v in input_constants_dict.iteritems():
    cinput.__dict__[k] = v

from linux_input import *

event_types = [EV_SYN, EV_KEY, EV_REL, EV_ABS, EV_MSC, EV_SW,
        EV_LED, EV_SND, EV_REP, EV_FF, EV_PWR, EV_FF_STATUS]

rdict = lambda x: dict(map(lambda (k, v): (v, k), x))

keys = filter(lambda (k, v): k.startswith("KEY_") or k.startswith("BTN_"),
    input_constants_dict.iteritems())
rev_keys = rdict(keys)

absaxes = filter(lambda (k, v): k.startswith("ABS_"),
    input_constants_dict.iteritems())
rev_absaxes = rdict(absaxes)

rel  = filter(lambda (k, v): k.startswith("REL_"),
    input_constants_dict.iteritems())
rev_rel = rdict(rel)

syn = filter(lambda (k, v): k.startswith("SYN_"),
    input_constants_dict.iteritems())
rev_syn = rdict(syn)

del rdict
