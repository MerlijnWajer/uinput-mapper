try:
    import json
except ImportError:
    import simplejson as json

class Pickler(object):
    def __init__(self, fd):
        self.fd = fd
        self.dumps = json.dumps

    def dump(self, dat):
        s = self.dumps(dat)

        self.fd.write('%.5d' % len(s))
        self.fd.write(s)

class Unpickler(object):
    def __init__(self, fd):
        self.fd = fd
        self.loads = json.loads

    def load(self):
        s = self.fd.read(5)

        if len(s) < 5:
            print 'Unexpected int size'


        toread = int(s)
        r = self.fd.read(toread)
        return self.loads(r, object_hook=hinted_tuple_hook)
