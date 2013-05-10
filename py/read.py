import linux_uinput, ctypes, fcntl, os, sys
from cinput import *
from mapper import KeyMapper, parse_conf
from example_conf import config

try:
    import cPickle as pickle
except ImportError:
    import pickle

import optparse

parser = optparse.OptionParser(description='Read input devices. '
        'TODO')
parser.add_option('-D', '--dump', action='store_false',
        default=True, help='Dump will marshall all the events to stdout')
parser.add_option('-i', '--input-file', action='append',
        type=str, default=[],
        help='Read events from this input device')

parser.add_option('-C', '--compat', action='store_true',
        help='Enable compatibility mode; for Python < 2.7')

args = parser.parse_args()


if len(args.input_file) == 0:
    parser.print_help()
    exit(0)

# TODO: Support multiple input files + epoll; InputDevices?
f = InputDevice(args.input_file[0])

config = parse_conf(f)
m = KeyMapper(config)

if args.dump:
    print 'Version:', f.get_version()
    print f.get_name()

    d = f.get_exposed_events()
    for k, v in d.iteritems():
        print k + ':', ', '.join(v)

else:
    p = pickle.Pickler(sys.stdout)

    p.dump(config)

    sys.stdout.flush()

while True:
    # TODO: Poll multiple files ; add file description (not descriptor...)
    # f, ev = fs.next_event()
    ev = f.next_event()

    if args.dump:
        try:
            print ev.time.tv_sec, ev.time.tv_usec
            s = '%s %s %d' % (rev_events[ev.type], rev_event_keys[ev.type][ev.code], ev.value)
            print 'Event type:', s
        except KeyError:
           pass

    else:
        if not args.compat:
            p.dump(ev)
        else:
            # Use this rather than the line above if you use an old python version (also
            # edit create.py)
            p.dump((ev.time.tv_sec, ev.time.tv_usec, ev.type, ev.code, ev.value))

        sys.stdout.flush()
