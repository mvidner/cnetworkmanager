from device import cDevice, cDeviceEth
from manager import NMI
from ap07 import cAP_07
from util import *
import dbus

class cDevice_07(cDevice):
    def DeviceType0(self):
        if self.dt is None:
            self.dt = self.get_property("DeviceType")
            if self.dt == 1:
                self.__class__ = cDeviceEth_07
            elif self.dt == 2:
                self.__class__ = cDeviceWifi_07
            elif self.dt == 3:
                self.__class__ = cDeviceGSM_07
        return self.dt

    NM_DEVICE_STATE = [
        "UNKNOWN", "UNMANAGED", "UNAVAILABLE", "DISCONNECTED", "PREPARE",
        "CONFIG", "NEED_AUTH", "IP_CONFIG", "ACTIVATED", "FAILED",]

    def Dump(self):
        cDevice.Dump(self)

        # "Ip4Config", only for NM_DEVICE_STATE_ACTIVATED
        self.dump_props(["Udi", "Interface", "Driver",])
        addr = self.get_property("Ip4Address")
        print "  Ip4Address:", self.ip_str(addr)
        caps = self.get_property("Capabilities")
        print "  Capabilities:", bitmask_str(self.NM_DEVICE_CAP, caps)
        state = self.NM_DEVICE_STATE[self.get_property("State")]
        print "  Dev State:", state
        if state == "ACTIVATED":
            self.DumpIp4Config(self.get_property("Ip4Config"))

        dt = self.DeviceType()
        print "  Dev Type:", dt
        self.DumpMore()

class cDeviceEth_07(cDevice_07, cDeviceEth):
    def DumpMore(self):
        self.dump_props(["HwAddress", "Speed", "Carrier"])

class cDeviceGSM_07(cDevice_07):
    def DumpMore(self):
        self.dump_props([])

class cDeviceWifi_07(cDevice_07):
    NM_802_11_DEVICE_CAP = {1:"CIPHER_WEP40", 2:"CIPHER_WEP104",
                            4:"CIPHER_TKIP", 8:"CIPHER_CCMP",
                            16:"WPA", 32:"RSN",}

    def APs(self):
        self.wdevi = dbus.Interface(self.obj, NMI + ".Device.Wireless")
        aps = self.wdevi.GetAccessPoints()
        return map(cAP_07, aps)

    def DumpMore(self):
        print "  Dev Mode:", self.IW_MODE[self.get_property("Mode")]
        wcaps = self.get_property("WirelessCapabilities")
        print "  Wifi Capabilities:", bitmask_str(self.NM_802_11_DEVICE_CAP, wcaps)
        self.dump_props(["HwAddress", "Bitrate", "ActiveAccessPoint"])
#FIXME pass options otherwise
#        if self.options.ap:
        if True:
            print "  Access Points"
            for ap in self.APs():
                ap.Dump()
    
