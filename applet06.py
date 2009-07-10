from connection06 import cConnection_06
from applet import cApplet

NETWORK_TYPE_ALLOWED = 1
class cApplet_06(cApplet):
    def __init__(self, svc, opath):
        self.svc = svc
        self.opath = opath
        self.io = bus.get_object(self.svc, self.opath)
        self.ii = dbus.Interface(self.io, 'org.freedesktop.NetworkManagerInfo')

    def isSystem(self):
        return False;

    def myConnection(self, opath):
        return cConnection_06(self, opath)

    # TODO also VPN conns
    def Connections(self):
        names = self.ii.getNetworks(NETWORK_TYPE_ALLOWED)
        return map(self.myConnection, names)

