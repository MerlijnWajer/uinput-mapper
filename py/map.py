import cinput
import ctypes

f = open("/dev/input/event5")


while True:
    #print ctypes.sizeof(input.input_event)
    hoi = f.read(ctypes.sizeof(cinput.input_event))
    #print repr(hoi)

    e = ctypes.cast(hoi, ctypes.POINTER(cinput.input_event))
    ev = e.contents

    keys = filter(lambda (k, v): k.startswith("KEY_") or k.startswith("BTN_"),
        cinput.input_constants_dict.iteritems())

    if ev.type == cinput.EV_KEY:
        for k, v in keys:
            if v == ev.code:
                print k
        #print e.contents.type
        #print e.contents.code
        #print e.contents.value

