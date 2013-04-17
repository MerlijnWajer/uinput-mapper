import cinput

from gen import input_constants_dict

for k, v in input_constants_dict.iteritems():
    cinput.__dict__[k] = v

from linux_input import *
