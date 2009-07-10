import dbus.service
from svc_settings import UserSettings

class UserSettings_06(UserSettings):
    # conmaps is a list
    def __init__(self, opath, conmaps):
        dbus.service.Object.__init__(self, bus, opath)
        #print "CONMAPS:", conmaps
        self.conns = map(self.newCon, conmaps)

    counter = 1
    def newCon(self, conmap):
        cpath = "/MyConnection/%d" % self.counter
        self.counter = self.counter + 1
        c = Connection_06(cpath, conmap)
        #self.NewConnection(cpath) # announce it
        return c

    @dbus.service.method(dbus_interface="org.freedesktop.NetworkManagerInfo",
                         in_signature="i", out_signature='as')
    def getNetworks(self, i):
        # FIXME bytearray to str WHERE?
        #n = [ssid_str(c.Ssid()) for c in self.conns]
        n = [c.ID() for c in self.conns]
        print "getNetworks:", n
        return n

    @dbus.service.method(dbus_interface="org.freedesktop.NetworkManagerInfo",
                         in_signature="", out_signature='ao') # out??
    def getVPNConnections(self):
        return []               # FIXME

    @dbus.service.method(dbus_interface="org.freedesktop.NetworkManagerInfo",
                         in_signature="si")
                         #out_signature='sibasi') #varies
    def getNetworkProperties(self, net, type):
        print "GNP", net
        # type is 1, NETWORK_TYPE_ALLOWED
        c = self.GetByNet(net)
        if c != None:
            return c.getNetworkProperties()
        print "Oops, could not getNetworkProperties for " + net
        

    @dbus.service.method(dbus_interface="org.freedesktop.NetworkManagerInfo",
                         in_signature="oosib")
                         #out_signature="isi") varies
    def getKeyForNetwork(self, dev, net, ssid, attempt, newkey):
        print "GKFN", dev, net, ssid, attempt, bool(newkey)
        if newkey:
            m = "Cannot ask for key"
            print m
            raise dbus.exceptions.DBusException(m)

        snet = opath_unescape(net[net.rfind("/")+1 : ]) # only stuff after /
        c = self.GetByNet(snet)
        if c != None:
            return c.getKeyForNetwork()
        print "Oops, could not getKeyForNetwork " + net

    @dbus.service.method(dbus_interface="org.freedesktop.NetworkManagerInfo",
                         out_signature='')
                         #in_signature="sbs isi", varies
    def updateNetworkInfo(self, ssid, automatic, bssid, *security):
        print "Connected successfully"
        return
        print "UNI"
        print " ssid:", ssid
        print " automatic:", bool(automatic)
        print " bssid:", bssid
        print " security:", security


    def GetByNet(self, net_name):
        "Returns connection, or None"
        for c in self.conns:
            if c.isNet(net_name):
                return c
        return None


