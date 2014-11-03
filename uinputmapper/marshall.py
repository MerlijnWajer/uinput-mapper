import jsonmarshall

try:
    import cPickle as pickle
except ImportError:
    import pickle

import literalevalmarshall

def Pickler(fd, t):
    return { 'pickle': pickle.Pickler(fd),
             'json' : jsonmarshall.Pickler(fd),
             'literaleval' : literalevalmarshall.Pickler(fd)
           }[t]

def Unpickler(fd, t):
    return { 'pickle': pickle.Unpickler(fd),
             'json' : jsonmarshall.Unpickler(fd),
             'literaleval' : literalevalmarshall.Unpickler(fd)
           }[t]
