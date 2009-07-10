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
