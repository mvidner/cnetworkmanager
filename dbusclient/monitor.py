"A simple abbreviating monitor of DBus signals"

import string

class Monitor(object):
    """A Base for printing signals on the bus.

    It uses add_signal_receiver"""

    __docformat__ = "epytext en"

    # TODO self is probably superfluous,
    # this could be a module instead of a class?
    def __init__(self, bus):
        """Watch on I{bus}, eg. dbus.SystemBus()"""

        self.bus = bus
        self.amap = {}
        self.specific = {}
        self.bus.add_signal_receiver(self._abbr_h,
                        path_keyword="path",
                        interface_keyword="interface",
                        member_keyword="member")

    def ignore(self, dbus_interface, signal_name):
        """Ignore a signal, do not use the default _abbr_h on it.

        Instead, use _null_h."""

        self.watch(self._null_h, dbus_interface, signal_name)

    def _null_h(self, *args, **kwargs):
        "The null handler, does nothing."

        pass

    def watch(self, handler, dbus_interface, signal_name):
        """Add a specific handler for a signal."""

        self.specific[dbus_interface +"."+ signal_name] = True
        self.bus.add_signal_receiver(handler,
                                dbus_interface=dbus_interface,
                                signal_name=signal_name,
                                path_keyword="path")

    def _abbr_h(self, *args, **kwargs):
        """The generic abbreviating handler.

        It handles all signals, but it checks if a specific handler was
        installed by watch and does nothing in such case."""

        ifc = kwargs["interface"]
        sig = kwargs["member"]
        if self.specific.has_key(ifc +"."+ sig):
            return

        opath = kwargs["path"]
        line = "SIG %s: %s.%s%s" % (self._abbrev(opath,"/"),
                                    self._abbrev(ifc,"."),
                                    sig, args)
        print line

    def _abbrev(self, s, sep):
        """Prints an abbreviation of s (whose components are separated by sep).

        It remembers what is abbreviated how and notifies if there is
        a collision.
        """
        words = s.split(sep)
        words = map (self._a1, words)
        result = sep.join(words)
        if self.amap.has_key(result):
            if self.amap[result] != s:
                print "ABBR COLLISION %s was %s now %s" % (result, self.amap[result], s)
        else:
            print "ABBR %s is %s" % (result, s)
        self.amap[result] = s
        return result
    
    def _a1(self, s):
        """Abbreviates a single component.

        First character is unchanged, delete lowercase and _ from the rest.
        """

        if s == "":
            return ""
        #print "#A", s
        return s[0] + s[1:].translate(string.maketrans("", ""),
                                      string.lowercase + "_")
