import dbus
from object import *
from manager import *
from connection import cConnection

SSC = "org.freedesktop.NetworkManagerSystemSettings"
USC = "org.freedesktop.NetworkManagerUserSettings"
NMIC = "org.freedesktop.NetworkManagerInfo"

# this is the client side of the applet; see also UserSettings
class cApplet(cObject):
    def __init__(self, svc, opath):
        cObject.__init__(self, opath, svc)
        self.si = dbus.Interface(self.obj, 'org.freedesktop.NetworkManagerSettings')

    def prop_iface(self):
        return NMI

    def isSystem(self):
        return self.svc == SSC;

    def Dump(self):
        for conn in self.Connections():
            conn.Dump()
        if self.isSystem():
            self.DumpSystem()

    def DumpSystem(self):
        print "Unmanaged Devices"
        umds = self.get_property("UnmanagedDevices")
        for umd in umds:
            print " ", umd
           #  dump_settings_conn(svc, conn) umd?


    def myConnection(self, opath):
        return cConnection(self.svc, opath)

    def Connections(self):
        opaths = self.si.ListConnections()
        return map(self.myConnection, opaths)

