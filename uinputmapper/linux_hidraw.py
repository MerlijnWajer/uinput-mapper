import ctypes
import struct
from ioctlhelp import IOR, IOW, IOC, IO, _IOC_READ


# --- HID ---

USB_INTERFACE_CLASS_HID = 3

USB_INTERFACE_SUBCLASS_BOOT = 1
USB_INTERFACE_PROTOCOL_KEYBOARD = 1
USB_INTERFACE_PROTOCOL_MOUSE = 2

HID_REQ_GET_REPORT = 0x01
HID_REQ_GET_IDLE = 0x02
HID_REQ_GET_PROTOCOL = 0x03
HID_REQ_SET_REPORT = 0x09
HID_REQ_SET_IDLE = 0x0A
HID_REQ_SET_PROTOCOL = 0x0B

#HID_DT_HID =			(USB_TYPE_CLASS | 0x01)
#HID_DT_REPORT =			(USB_TYPE_CLASS | 0x02)
#HID_DT_PHYSICAL =			(USB_TYPE_CLASS | 0x03)

HID_MAX_DESCRIPTOR_SIZE = 4096

# --- HIDDEV ---

class hiddev_event(ctypes.Structure):
    _fields_ = [
        ("hid", ctypes.c_uint32),
        ("value", ctypes.c_int32)
    ]

class hiddev_devinfo(ctypes.Structure):
    _fields_ = [
        ("bustype", ctypes.c_uint32),
        ("busnum", ctypes.c_uint32),
        ("devnum", ctypes.c_uint32),
        ("ifnum", ctypes.c_uint32),
        ("vendor", ctypes.c_int16),
        ("product", ctypes.c_int16),
        ("num_applications", ctypes.c_uint32)
    ]

class hiddev_collection_info(ctypes.Structure):
    _fields_ = [
        ("index", ctypes.c_uint32),
        ("type", ctypes.c_uint32),
        ("usage", ctypes.c_uint32),
        ("level", ctypes.c_uint32)
    ]

HID_STRING_SIZE = 256
class hiddev_string_descriptor(ctypes.Structure):
    _fields_ = [
        ("index", ctypes.c_int32),
        ("value", ctypes.c_char * HID_STRING_SIZE)
    ]

class hiddev_report_info(ctypes.Structure):
    _fields_ = [
        ("report_type", ctypes.c_uint32),
        ("report_id", ctypes.c_uint32),
        ("num_fields", ctypes.c_uint32)
    ]

HID_REPORT_ID_UNKNOWN = 0xffffffff
HID_REPORT_ID_FIRST   = 0x00000100
HID_REPORT_ID_NEXT    = 0x00000200
HID_REPORT_ID_MASK    = 0x000000ff
HID_REPORT_ID_MAX     = 0x000000ff

HID_REPORT_TYPE_INPUT	= 1
HID_REPORT_TYPE_OUTPUT	= 2
HID_REPORT_TYPE_FEATURE	= 3
HID_REPORT_TYPE_MIN     = 1
HID_REPORT_TYPE_MAX     = 3

class hiddev_field_info(ctypes.Structure):
    _fields_ = [
        ("report_type", ctypes.c_uint32),
        ("report_id", ctypes.c_uint32),
        ("field_index", ctypes.c_uint32),
        ("maxusage", ctypes.c_uint32),
        ("flags", ctypes.c_uint32),
        ("physical", ctypes.c_uint32),
        ("logical", ctypes.c_uint32),
        ("application", ctypes.c_uint32),
        ("logical_minumum", ctypes.c_int32),
        ("logical_maximum", ctypes.c_int32),
        ("physical_minimum", ctypes.c_int32),
        ("physical_maximum", ctypes.c_int32),
        ("unit_exponent", ctypes.c_int32),
        ("unit", ctypes.c_int32)
    ]

HID_FIELD_CONSTANT		= 0x001
HID_FIELD_VARIABLE		= 0x002
HID_FIELD_RELATIVE		= 0x004
HID_FIELD_WRAP			= 0x008
HID_FIELD_NONLINEAR		= 0x010
HID_FIELD_NO_PREFERRED	= 0x020
HID_FIELD_NULL_STATE	= 0x040
HID_FIELD_VOLATILE		= 0x080
HID_FIELD_BUFFERED_BYTE	= 0x100

class hiddev_usage_ref(ctypes.Structure):
    pass

class hiddev_usage_ref_multi(ctypes.Structure):
    pass

HID_FIELD_INDEX_NONE = 0xffffffff
HID_VERSION	= 0x010004

# HIDIOCGVERSION		_IOR('H', 0x01, int)
HIDIOCGVERSION = IOR(ord('H'), 0x01, '@i')

# HIDIOCAPPLICATION	_IO('H', 0x02)
HIDIOCAPPLICATIO = IO(ord('H'), 0x02)
# HIDIOCGDEVINFO		_IOR('H', 0x03, struct hiddev_devinfo)
HIDIOCGDEVINFO = IOR(ord('H'), 0x03, ctypes.sizeof(hiddev_devinfo))

# HIDIOCGSTRING		_IOR('H', 0x04, struct hiddev_string_descriptor)
HIDIOCGSTRING = IOR(ord('H'), 0x04, ctypes.sizeof(hiddev_string_descriptor))

# HIDIOCINITREPORT	_IO('H', 0x05)
HIDIOCINITREPORT = IO(ord('H'), 0x05)

HIDIOCGNAME = lambda _l: IOC(_IOC_READ, ord('H'), 0x06, struct.calcsize('%ds' % _l))

# HIDIOCGREPORT		_IOW('H', 0x07, struct hiddev_report_info)
# HIDIOCSREPORT		_IOW('H', 0x08, struct hiddev_report_info)
# HIDIOCGREPORTINFO	_IOWR('H', 0x09, struct hiddev_report_info)
# HIDIOCGFIELDINFO	_IOWR('H', 0x0A, struct hiddev_field_info)
# HIDIOCGUSAGE		_IOWR('H', 0x0B, struct hiddev_usage_ref)
# HIDIOCSUSAGE		_IOW('H', 0x0C, struct hiddev_usage_ref)
# HIDIOCGUCODE		_IOWR('H', 0x0D, struct hiddev_usage_ref)
# HIDIOCGFLAG		_IOR('H', 0x0E, int)
# HIDIOCSFLAG		_IOW('H', 0x0F, int)
# HIDIOCGCOLLECTIONINDEX	_IOW('H', 0x10, struct hiddev_usage_ref)
# HIDIOCGCOLLECTIONINFO	_IOWR('H', 0x11, struct hiddev_collection_info)
# HIDIOCGPHYS(len)	_IOC(_IOC_READ, 'H', 0x12, len)

# HIDIOCGUSAGES		_IOWR('H', 0x13, struct hiddev_usage_ref_multi)
# HIDIOCSUSAGES		_IOW('H', 0x14, struct hiddev_usage_ref_multi)

HIDDEV_FLAG_UREF	= 0x1
HIDDEV_FLAG_REPORT	= 0x2
HIDDEV_FLAGS		= 0x3


def get_hid_version(f):
    buf = array.array('i', [0])
    r = fcntl.ioctl(f, HIDIOCGVERSION, buf)
    v = buf.tolist()[0]
    #return "%d" % v
    return "%d.%d.%d" % ( v >> 16, (v >> 8) & 0xff, v & 0xff)

# --- HID RAW ---



HID_STRING_SIZE = 256
class hidraw_report_descriptor(ctypes.Structure):
    _fields_ = [
        ("size", ctypes.c_uint32),
        ("_value", ctypes.c_uint8 * HID_MAX_DESCRIPTOR_SIZE)
    ]

class hidraw_devinfo(ctypes.Structure):
    _fields_ = [
        ("bustype", ctypes.c_uint32),
        ("vendor", ctypes.c_int16),
        ("product", ctypes.c_int16)
    ]

#define HIDIOCGRDESCSIZE    _IOR('H', 0x01, int)
HIDIOCGRDESCSIZE = IOR(ord('H'), 0x01, '@i')

#define HIDIOCGRDESC        _IOR('H', 0x02, struct hidraw_report_descriptor)
HIDIOCGRDESC = IOR(ord('H'), 0x02, ctypes.sizeof(hidraw_report_descriptor))

#define HIDIOCGRAWINFO      _IOR('H', 0x03, struct hidraw_devinfo)
HIDIOCGRAWINFO = IOR(ord('H'), 0x03, ctypes.sizeof(hidraw_devinfo))

#define HIDIOCGRAWNAME(len)     _IOC(_IOC_READ, 'H', 0x04, len)
HIDIOCGRAWNAME = lambda _l: IOC(_IOC_READ, ord('H'), 0x04, struct.calcsize('%ds' %  _l))

#define HIDIOCGRAWPHYS(len)     _IOC(_IOC_READ, 'H', 0x05, len)
HIDIOCGRAWPHYS = lambda _l: IOC(_IOC_READ, ord('H'), 0x05, struct.calcsize('%ds' % _l))

#define HIDIOCSFEATURE(len)    _IOC(_IOC_WRITE|_IOC_READ, 'H', 0x06, len)
HIDIOCSFEATURE = lambda _l : IOC(_IOC_WRITE|_IOC_READ, ord('H'), 0x06, struct.calcsize('%ds' % _l))

#define HIDIOCGFEATURE(len)    _IOC(_IOC_WRITE|_IOC_READ, 'H', 0x07, len)
HIDIOCGFEATURE = lambda _l: IOC(_IOC_WRITE|_IOC_READ, ord('H'), 0x07, struct.calcsize('%ds' % _l))

HIDRAW_FIRST_MINOR = 0
HIDRAW_MAX_DEVICES = 64
HIDRAW_BUFFER_SIZE = 64

def get_hidraw_name(f, l=99):
    buf = array.array('c', ' ' * l)
    r = fcntl.ioctl(f, HIDIOCGRAWNAME(l), buf)

    return ''.join(buf.tolist()[:r])

def get_devinfo(f):
    buf = (hidraw_devinfo * 1)()
    r = fcntl.ioctl(f, HIDIOCGRAWINFO, buf)
    v = buf[0]
    return map(hex, (v.bustype, v.vendor, v.product))

def get_report_descriptor(f):
    buf = ctypes.c_int32()
    r = fcntl.ioctl(f, HIDIOCGRDESCSIZE, buf)
    l = buf.value

    buf = hidraw_report_descriptor()
    buf.size = l
    r = fcntl.ioctl(f, HIDIOCGRDESC, buf)

    return [hex(buf._value[_]) for _ in range(l)]

def read_ev(f):
    estr = os.read(f, ctypes.sizeof(hiddev_event))

    e = ctypes.cast(estr, ctypes.POINTER(hiddev_event))
    ev = e.contents

    return hiddev_event(ev.hid, ev.value)

if __name__ == '__main__':
    import os, fcntl, sys, array, struct

    f = os.open("/dev/hidraw1", os.O_RDONLY)

    print get_hid_version(f)
    print get_hidraw_name(f)

    print get_devinfo(f)

    print get_report_descriptor(f)

    while 1:
        e = read_ev(f)
        print e.hid, e.value

