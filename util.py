import string
import re
import time

def bitmask_str(map, value):
    ret = []
    for mask in sorted(map.keys()):
        if value & mask: ret.append(map[mask])
    return ",".join(ret)

def ssid_str(array):
    s = ""
    for b in array:
        s = s + ("%c" % b)
    return s

def opath_validchar(c):
    # _ is also escaped even though it is valid
    return \
        string.ascii_letters.find(c) != -1 or \
        string.digits.find(c) != -1

def opath_escape(s):
    r = ""
    for c in s:
        # TODO find a more elegant way
        if not opath_validchar(c):
            # "-" -> "_2d_"
            c = "_%2x_" % ord(c)
        r = r + c
    return r

def opath_unescape(s):
    # "2d" -> "-"
    unhex = lambda xx: chr(eval("0x"+xx))
    # all "_2d_" -> "-"
    return re.sub("_.._", lambda p: unhex(p.group()[1:3]), s)

def dump_time(unixtime):
    return time.asctime(time.localtime(unixtime))

