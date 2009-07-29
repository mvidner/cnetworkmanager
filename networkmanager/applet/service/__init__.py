import dbus
import dbus.service
from connection import Connection

# server analog of cApplet
class UserSettings(dbus.service.Object):
    # conmaps is a list
    def __init__(self, opath, conmaps):
        bus = dbus.SystemBus()
        dbus.service.Object.__init__(self, bus, opath)
        #print "CONMAPS:", conmaps
        self.conns = map(self.newCon, conmaps)

    def addCon(self, conmap):
        c = self.newCon(conmap)
        self.conns.append(c)
        return c

    counter = 1
    def newCon(self, conmap):
        cpath = "/MyConnection/%d" % self.counter
        self.counter = self.counter + 1
        c = Connection(cpath, conmap)
        self.NewConnection(cpath) # announce it
        return c

    @dbus.service.method(dbus_interface='org.freedesktop.NetworkManagerSettings',
                             in_signature='', out_signature='ao')
    def ListConnections(self):
        return [c.__dbus_object_path__ for c in self.conns]

    #this is for EMITTING a signal, not receiving it
    @dbus.service.signal(dbus_interface='org.freedesktop.NetworkManagerSettings',
                             signature='o')
    def NewConnection(self, opath):
        pass
        #print "signalling newconn:", opath

    def GetByNet(self, net_name):
        "Returns connection, or None"
        for c in self.conns:
            if c.isNet(net_name):
                return c
        return None


