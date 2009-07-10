from manager import cNM, NMI
from object import *
from device07 import cDevice_07

class cNM_07(cNM):
    def Api(self):
        return "07"

    def SetWifiEnabled(self, v):
        self.set_property("WirelessEnabled", v)

    def SetOnline(self, v):
        self.nmi.Sleep(not v)

    def Dump0(self):
        print "State:", self.NM_STATE[self.get_property("State")]
        print "Wifi enabled:", self.get_property("WirelessEnabled")
        print "Wifi HW enabled:", self.get_property("WirelessHardwareEnabled")

    def Devices(self):
        opaths = self.nmi.GetDevices()
        return map(cDevice_07, opaths)

    def ActiveConnections(self):
        aconns = self.get_property("ActiveConnections")
        return map(cActiveConnection, aconns)

    def ActivateConnection(self, conn, device, ap):
        # passing *_handler makes the call asynchronous
        self.nmi.ActivateConnection(USC,
                                    conn.__dbus_object_path__,
                                    device.opath,
                                    ap.opath,
                                    reply_handler=self.silent_handler,
                                    error_handler=self.err_handler,
                                    )

class cActiveConnection(cObject):
    def __init__(self, opath):
        cObject.__init__(self, opath)

    def get_property(self, property_name):
        return cObject.get_property(self, NMI, property_name)

    def Dump(self):
       print self.opath
       for P in ["ServiceName", "Connection", "SpecificObject",]:
           print "  %s: %s" % (P, self.get_property(P))
       devs = self.get_property("Devices")
       print "  Devices:"
       for dev in devs:
           print "  ", dev
   
