import dbus
import dbus.service
import _dbus_bindings
from connection import Connection
from networkmanager.base import Bus
from networkmanager.applet import USER_SERVICE, SYSTEM_SERVICE

def service_pid(name):
    bus = Bus()
    DBS = 'org.freedesktop.DBus'
    DBI = DBS
    dbo = bus.get_object(DBS, '/')
    dbi = dbus.Interface(dbo, DBI)
    owner = dbi.GetNameOwner(name)
    pid = dbi.GetConnectionUnixProcessID(owner)
    return pid

# server analog of cApplet
class NetworkManagerSettings(dbus.service.Object):
    # conmaps is a list
    def __init__(self, conmaps, requested_name = None):
        bus = Bus()
        opath = "/org/freedesktop/NetworkManagerSettings"
        bus_name = None
        if requested_name != None:
            NEE = dbus.exceptions.NameExistsException
            try:
                bus_name = dbus.service.BusName(requested_name, bus,
                                                replace_existing=True,
                                                do_not_queue=True)
            except NEE:
                raise  NEE("%s (pid %d)" % (requested_name, service_pid(requested_name)))
        dbus.service.Object.__init__(self, bus, opath, bus_name)
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

class NetworkManagerUserSettings(NetworkManagerSettings):
    def __init__(self, conmaps):
        super(NetworkManagerUserSettings, self).__init__(conmaps, USER_SERVICE)

# probably does not make sense to reimplement system settings
# but anyway, just for symmetry
class NetworkManagerSystemSettings(NetworkManagerSettings):
    def __init__(self, conmaps):
        super(NetworkManagerSystemSettings, self).__init__(conmaps, SYSTEM_SERVICE)

Applet = NetworkManagerSettings
UserApplet = NetworkManagerUserSettings
SystemApplet = NetworkManagerSystemSettings
