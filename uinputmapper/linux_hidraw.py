import ctypes
import struct
from ioctlhelp import IOR, IOW, IOC, IO, _IOC_READ

class hiddev_event(ctypes.Structure):
    _fields_ = [
        ("hid", ctypes.c_uint32),
        ("value", ctypes.c_int32)
    ]

class hiddev_devinfo(ctypes.Structure):
    pass
