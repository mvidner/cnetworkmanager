from device import cDevice, cDeviceEth
from ap import cAP
from util import *

class cAP_07(cAP):
    def Mbr(self):
        return self.get_property("MaxBitrate")

    def PrivS(self):
        priv = self.get_property("Flags") != 0
        wpa = self.get_property("WpaFlags") != 0
        wpa2 = self.get_property("RsnFlags") != 0
        priv_s = ""
        if priv:
            if not wpa and not wpa2:
                priv_s = priv_s + " WEP"
            if wpa:
                priv_s = priv_s + " WPA"
            if wpa2:
                priv_s = priv_s + " WPA2"
        return priv_s

    def Strength(self):
        return int(self.get_property("Strength"))

    def Ssid(self):
        return ssid_str(self.get_property("Ssid"))

    def Dump(self):
        print "  AP:", self.opath
        print "    Ssid:", self.Ssid()
        for P in ["Frequency", "HwAddress", "MaxBitrate",]:
            print "    %s: %s" % (P, self.get_property(P))
        print "    Strength:", self.Strength()
        print "    AP Mode:", cDevice.IW_MODE[self.get_property("Mode")]
        print "    AP Flags:", bitmask_str(self.NM_802_11_AP_FLAGS,
                                           self.get_property("Flags"))
        print "    AP WPA Flags:", bitmask_str(self.NM_802_11_AP_SEC,
                                               self.get_property("WpaFlags"))
        print "    AP RSN Flags:", bitmask_str(self.NM_802_11_AP_SEC,
                                               self.get_property("RsnFlags"))
    
