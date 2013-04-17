import ctypes

# structure

"""
struct input_event {
    struct timeval time;
    __u16 type;
    __u16 code;
    __s32 value;
};
"""

class timeval(ctypes.Structure):
    _fields_ = [("tv_sec", ctypes.c_long), ("tv_usec", ctypes.c_long)]

class input_event(ctypes.Structure):
    _fields_ = [
        ("time", timeval),
        ("type", ctypes.c_uint16),
        ("code", ctypes.c_uint16),
        ("value", ctypes.c_int32)
    ]

