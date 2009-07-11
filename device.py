from object import *
from manager import NMI

class cDevice(cObject):
    def __init__(self, opath):
        cObject.__init__(self, opath)
        self.devi = dbus.Interface(self.obj, NMI + ".Device")
        self.dt = None
        self.DeviceType0()

    def prop_iface(self):
        return NMI

    DEVICE_TYPE = ["UNKNOWN", "802_3_ETHERNET", "802_11_WIRELESS",
                   "GSM", "CDMA",] #OLPC: 3 is MESH

    def DeviceType(self):
        return self.DEVICE_TYPE[self.DeviceType0()]

    def ip_str(self, i32):
        ret = []
        ret.append("%d" % (i32 % 256))
        i32 /= 256
        ret.append("%d" % (i32 % 256))
        i32 /= 256
        ret.append("%d" % (i32 % 256))
        i32 /= 256
        ret.append("%d" % (i32 % 256))
        i32 /= 256
        return ".".join(ret)

    # TODO new class
    def DumpIp4Config(self, opath):
        print "   Ip4Config:", opath
        o = self.bus.get_object(NMC, opath)
        pi = dbus.Interface(o, PI)
        try:
            for P in ["Address", "Netmask", "Broadcast", "Gateway",]: # beta2?
                print "    %s: %s" % (P, self.ip_str(pi.Get(NMI, P)))
        except:
            print "    Addresses:"
            addrs = pi.Get(NMI, "Addresses")
            for addr in addrs:
                print "     %s/%s via %s" %  tuple(map(self.ip_str, addr))
        nss = pi.Get(NMI, "Nameservers")
        print "    Nameservers:", " ".join(map(self.ip_str, nss))
        doms = pi.Get(NMI, "Domains")
        print "    Domains:", " ".join(doms)

    NM_DEVICE_CAP = {1: "NM_SUPPORTED", 2: "CARRIER_DETECT", 4: "SCANNING", }

    
    def Dump(self):
        print "Device:", self.opath


    IW_MODE = ["AUTO", "ADHOC", "INFRA", "MASTER",
               "REPEAT", "SECOND", "MONITOR",]

    def APs(self):
        return []

    def ListNets(self):
            for ap in self.APs():
                ap.ListNets()

# mixin
class cDeviceEth:
    pass
