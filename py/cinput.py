#TODO: remove this soon

from gen import input_constants_dict as icd

# TODO: Just combine linux_input and cinput and use locals() to set the
# variables rather than the silly hack
for k, v in icd.iteritems():
    locals()[k] = v

from linux_input import *


rdict = lambda x: dict(map(lambda (k, v): (v, k), x))

events = filter(lambda (k, v): k in ["EV_SYN", "EV_KEY", "EV_REL",
    "EV_ABS", "EV_MSC", "EV_SW", "EV_LED", "EV_SND", "EV_REP",
    "EV_FF", "EV_PWR", "EV_FF_STATUS"], icd.iteritems())
rev_events = rdict(events)


# TODO: Get proper ``names'' like evtest:
"""
static const char * const * const names[EV_MAX + 1] = {
	[0 ... EV_MAX] = NULL,
	[EV_SYN] = events,			[EV_KEY] = keys,
	[EV_REL] = relatives,			[EV_ABS] = absolutes,
	[EV_MSC] = misc,			[EV_LED] = leds,
	[EV_SND] = sounds,			[EV_REP] = repeats,
	[EV_SW] = switches,
	[EV_FF] = force,			[EV_FF_STATUS] = forcestatus,
};
"""

keys = filter(lambda (k, v): k.startswith("KEY_") or k.startswith("BTN_"),
    icd.iteritems())
rev_keys = rdict(keys)

absaxes = filter(lambda (k, v): k.startswith("ABS_"),
    icd.iteritems())
rev_absaxes = rdict(absaxes)

rel  = filter(lambda (k, v): k.startswith("REL_"),
    icd.iteritems())
rev_rel = rdict(rel)

syn = filter(lambda (k, v): k.startswith("SYN_"),
    icd.iteritems())
rev_syn = rdict(syn)

del rdict

misc = {}

leds = sounds = repeats = switches = force = forcestatus = None

event_keys = {
        EV_SYN: rev_syn,
        EV_KEY: rev_keys,
        EV_REL: rev_rel,
        EV_ABS: rev_absaxes,
        EV_MSC: misc,
        EV_LED: leds,
        EV_SND: sounds,
        EV_REP: repeats,
        EV_SW:  switches,
        EV_FF:  force,
        EV_FF_STATUS: forcestatus

}
