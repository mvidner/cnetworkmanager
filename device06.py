from device import cDevice, cDeviceEth

class cDevice_06(cDevice):
    def DeviceType0(self):
        if self.dt is None:
            self.dt = self.devi.getProperties()[2]
            if self.dt == 1:
                self.__class__ = cDeviceEth_06
            elif self.dt == 2:
                self.__class__ = cDeviceWifi_06
        return self.dt

    NM_ACT_STAGE = [
        "UNKNOWN", "DEVICE_PREPARE", "DEVICE_CONFIG", "NEED_USER_KEY",
        "IP_CONFIG_START", "IP_CONFIG_GET", "IP_CONFIG_COMMIT",
        "ACTIVATED", "FAILED", "CANCELLED", ]

    def Dump(self):
        cDevice.Dump(self)
        print "  Driver:", self.devi.getDriver()
        props = self.devi.getProperties() # osusb ussss sssii biuus as
        print "  Self:", props[0]         # o
        print "  Interface:", props[1]    # s
        print "  Type:", self.DEVICE_TYPE[props[2]] # u
        print "  UDI:", props[3]                    # s
        print "  Active:", bool(props[4])           # b
        print "  Activation Stage:", self.NM_ACT_STAGE[props[5]] # u
        print "  IP:", props[6]                     # s
        print "  Mask:", props[7]                   # s
        print "  Bcast:", props[8]                  # s
        print "  HwAddress:", props[9]              # s
        print "  GW:", props[10]                    # s
        print "  NS1:", props[11]                   # s
        print "  NS2:", props[12]                   # s
        self.DumpMore()

    def DumpMore(self):
	print "  (unknown device type, not dumping more)"

class cDeviceEth_06(cDevice_06, cDeviceEth):
    def DumpMore(self):
        props = self.devi.getProperties() # osusb ussss sssii biuus as
        print "  Link Active:", bool(props[15])     # b
        print "  Speed:", props[16]                 # i
        print "  Generic Capabilities:", bitmask_str(self.NM_DEVICE_CAP, props[17])  # u

class cDeviceWifi_06(cDevice_06):
    NM_802_11_CAP = {
	0x00000001: "PROTO_NONE",
	0x00000002: "PROTO_WEP",
	0x00000004: "PROTO_WPA",
	0x00000008: "PROTO_WPA2",
	0x00000010: "RESERVED1",
	0x00000020: "RESERVED2",
	0x00000040: "KEY_MGMT_PSK",
	0x00000080: "KEY_MGMT_802_1X",
	0x00000100: "RESERVED3",
	0x00000200: "RESERVED4",
	0x00000400: "RESERVED5",
	0x00000800: "RESERVED6",
	0x00001000: "CIPHER_WEP40",
	0x00002000: "CIPHER_WEP104",
	0x00004000: "CIPHER_TKIP",
	0x00008000: "CIPHER_CCMP",
        }

    def APs(self):
        self.wdevi = dbus.Interface(self.devo, NMI + ".Device.Wireless")
        aps = self.devi.getProperties()[20]
        return map(cAP_06, aps)

    def DumpMore(self):
        props = self.devi.getProperties() # osusb ussss sssii biuus as
        print "  Mode:", self.IW_MODE[props[13]]    # i
        print "  Strength:", props[14]              # i
        print "  Link Active:", bool(props[15])     # b
        print "  Speed:", props[16]                 # i
        print "  Generic Capabilities:", bitmask_str(self.NM_DEVICE_CAP, props[17])  # u
        print "  Capabilities:", bitmask_str(self.NM_802_11_CAP, props[18]) # u
        print "  Current net:", props[19]           # s
        nets = props[20]                            # as
        print "  Seen nets:", " ".join(nets)
        if options.ap:
            print "  Access Points"
            for ap in self.APs():
                ap.Dump()

