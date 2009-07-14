from device import cDevice, cDeviceEth
import device06
from ap import cAP
from util import *

class cAP_06(cAP):
    def Mbr(self, props=None):
        if props is None:
            props = self.devi.getProperties()
        return props[5]

    
    def PrivS(self):
        props = self.devi.getProperties()
        caps_s = bitmask_str(device06.cDeviceWifi_06.NM_802_11_CAP, props[7]) + ","
        priv_s = ""
        if caps_s.find("PROTO_WEP,") != -1:
            priv_s += " WEP"
        if caps_s.find("PROTO_WPA,") != -1:
            priv_s += " WPA"
        if caps_s.find("PROTO_WPA2,") != -1:
            priv_s += " WPA2"
        if caps_s.find("KEY_MGMT_802_1X,") != -1:
            priv_s += " Enterprise"
        return priv_s

    def Strength(self, props=None):
        if props is None:
            props = self.devi.getProperties()
        return props[3]

    def Ssid(self, props=None):
        if props is None:
            props = self.devi.getProperties()
        return props[1]


    def Dump(self):
        props = self.devi.getProperties() # ossid iiib
        print "   Self:", props[0]
        print "    Ssid:", self.Ssid(props)
        print "    HwAddress:", props[2]
        print "    Strength:", self.Strength(props)
        print "    Frequency:", props[4]
        print "    MaxBitrate:", self.Mbr(props)
        print "    AP Mode:", cDevice.IW_MODE[props[6]]
        print "    Capabilities:", bitmask_str(device06.cDeviceWifi_06.NM_802_11_CAP, props[7])
        print "    Broadcast:", props[8]
        
