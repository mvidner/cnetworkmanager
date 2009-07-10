from object import *
from manager import NMI

"""An AP found around us"""
class cAP(cObject):
    def __init__(self, opath):
        cObject.__init__(self, opath)
        # for _06
        self.devi = dbus.Interface(self.obj, NMI + ".Devices")

    def get_property(self, property_name):
        return cObject.get_property(self, NMI, property_name)

    def set_property(self, property_name, value):
        return cObject.set_property(self, NMI, property_name, value)

    NM_802_11_AP_FLAGS = {1: "PRIVACY",}

    NM_802_11_AP_SEC = {
        1: "PAIR_WEP40", 2: "PAIR_WEP104", 4: "PAIR_TKIP", 8: "PAIR_CCMP",
        16: "GROUP_WEP40", 32: "GROUP_WEP104", 64: "GROUP_TKIP",
        128: "GROUP_CCMP", 256: "KEY_MGMT_PSK", 512: "KEY_MGMT_802_1X",}

    def ListNets(self, marker = " "):
        # TODO *mark current
        mbr = self.Mbr() / 1024 # 07 1000, 06 1024?
        priv_s = self.PrivS()
        print "%s%3d: %s (%dMb%s)" % (marker, self.Strength(), self.Ssid(), mbr, priv_s)

