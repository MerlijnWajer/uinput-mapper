import ast

class Pickler(object):
    def __init__(self, fd):
        self.fd = fd

    def dump(self, dat):
        s = repr(dat)

        self.fd.write('%.5d' % len(s))
        self.fd.write(s)

class Unpickler(object):
    def __init__(self, fd):
        self.fd = fd

    def load(self):
        s = self.fd.read(5)

        if len(s) < 5:
            print 'Unexpected int size'


        toread = int(s)
        r = self.fd.read(toread)
        return ast.literal_eval(r)
