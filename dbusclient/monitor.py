import string

class Monitor(object):
    """A Base for printing signals on the bus"""

    def __init__(self, bus):
        self.bus = bus

        self.amap = {}
        self.specific = {}
        self.bus.add_signal_receiver(self.abbr_h,
                        path_keyword="path",
                        interface_keyword="interface",
                        member_keyword="member")

    def ignore(self, dbus_interface, signal_name):
        self.watch(self.null_h, dbus_interface, signal_name)

    def null_h(self, *args, **kwargs):
        pass

    def watch(self, handler, dbus_interface, signal_name):
        self.specific[dbus_interface +"."+ signal_name] = True
        self.bus.add_signal_receiver(handler,
                                dbus_interface=dbus_interface,
                                signal_name=signal_name,
                                path_keyword="path")

    def abbr_h(self, *args, **kwargs):
        ifc = kwargs["interface"]
        sig = kwargs["member"]
        if self.specific.has_key(ifc +"."+ sig):
            return

        opath = kwargs["path"]
        line = "SIG %s: %s.%s%s" % (self.abbrev(opath,"/"),
                                    self.abbrev(ifc,"."),
                                    sig, args)
        print line

    def abbrev(self, s, sep):
        words = s.split(sep)
        words = map (self.a1, words)
        result = sep.join(words)
        if self.amap.has_key(result):
            if self.amap[result] != s:
                print "ABBR COLLISION %s was %s now %s" % (result, self.amap[result], s)
        else:
            print "ABBR %s is %s" % (result, s)
        self.amap[result] = s
        return result
    
    def a1(self, s):
        if s == "":
            return ""
        #print "#A", s
        # first char, delete lowercase and _ from the rest
        return s[0] + s[1:].translate(string.maketrans("", ""),
                                      string.lowercase + "_")
