# -*- coding: utf-8 -*-
import dbus
from dbusclient import DBusClient
from dbusclient.func import *
import util

class Mode(util.Enum):
    UNKNOWN = 0
    ADHOC = 1
    INFRA = 2

class AccessPoint(DBusClient):
    """
    
     Signals:
    PropertiesChanged ( a{sv}: properties )
    
     Properties:
    Flags - u - (read) (NM_802_11_AP_FLAGS)
    WpaFlags - u - (read) (NM_802_11_AP_SEC)
    RsnFlags - u - (read) (NM_802_11_AP_SEC)
    Ssid - ay - (read)
    Frequency - u - (read)
    HwAddress - s - (read)
    Mode - u - (read) (NM_802_11_MODE)
    MaxBitrate - u - (read)
    Strength - y - (read)
    
     Sets of flags:
    NM_802_11_AP_FLAGS
    NM_802_11_AP_SEC
    """

    class Flags(util.Flags):
        NONE = 0x0
        PRIVACY = 0x1

    class Sec(util.Flags):
        NONE = 0x0
        PAIR_WEP40 = 0x1
        PAIR_WEP104 = 0x2
        PAIR_TKIP = 0x4
        PAIR_CCMP = 0x8
        GROUP_WEP40 = 0x10
        GROUP_WEP104 = 0x20
        GROUP_TKIP = 0x40
        GROUP_CCMP = 0x80
        KEY_MGMT_PSK = 0x100
        KEY_MGMT_802_1X = 0x200

    SERVICE = "org.freedesktop.NetworkManager"
    IFACE = "org.freedesktop.NetworkManager.AccessPoint"

    def __init__(self, opath):
        super(AccessPoint, self).__init__(dbus.SystemBus(), self.SERVICE, opath, default_interface=self.IFACE)

AccessPoint._add_adaptors(
#    PropertiesChanged = SA(identity),
    Flags = PA(AccessPoint.Flags),
    WpaFlags = PA(AccessPoint.Sec),
    RsnFlags = PA(AccessPoint.Sec),
    Ssid = PA(compose_ocers("".join, seq_adaptor(chr))), # byte array->str
#    Frequency = PA(identity),
#    HwAddress = PA(identity),
    Mode = PA(Mode),
#    MaxBitrate = PA(identity),
    Strength = PA(int),
    )
