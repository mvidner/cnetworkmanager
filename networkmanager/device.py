# -*- coding: utf-8 -*-

import dbus
#from networkmanager import NetworkManager
from dbusclient import DBusClient
from util import Enum, Flags
from func import *
from accesspoint import AccessPoint, Mode # for Wireless

class Ip4Address:
    def __init__(self, int32):
        self.a = int32
    def __str__(self):
        ret = []
        i32 = self.a
        for i in (1, 2, 3, 4):
            ret.append("%d" % (i32 % 256))
            i32 /= 256
        return ".".join(ret)
            
class Ip4Config(DBusClient):
    """
     Properties:    
    Addresses - aau - (read)
    Nameservers - au - (read)
    Domains - as - (read)
    Routes - aau - (read)
    """

    DBusClient._add_adaptors({
            "properties": {
                "Addresses": identity, #TODO
                "Nameservers": seq_adaptor(Ip4Address),
                #"Domains": identity,
                "Routes": identity, #TODO
                },
            })

    SERVICE = "org.freedesktop.NetworkManager"
    IFACE = "org.freedesktop.NetworkManager.Ip4Config"

    def __init__(self, opath):
        super(Ip4Config, self).__init__(dbus.SystemBus(), self.SERVICE, opath, default_interface = self.IFACE)

class Dhcp4Config(DBusClient):
    """
     Signals:
    PropertiesChanged ( a{sv}: properties )
     Properties:   
    Options - a{sv} - (read)
    """

    DBusClient._add_adaptors({
            "signals": {
                "PropertiesChanged": (identity, [identity], {}),
                },
            "properties": {
                "Options": identity,
                },
            })

    SERVICE = "org.freedesktop.NetworkManager"
    IFACE = "org.freedesktop.NetworkManager.Dhcp4Config"

    def __init__(self, opath):
        super(Dhcp4Config, self).__init__(dbus.SystemBus(), self.SERVICE, opath, default_interface = self.IFACE)

class Device(DBusClient):
    """networkmanager device
    
     Signals:
    StateChanged ( u: new_state, u: old_state, u: reason )
    
     Properties:
    Udi - s - (read)
    Interface - s - (read)
    Driver - s - (read)
    Capabilities - u - (read) (NM_DEVICE_CAP)
    Ip4Address - i - (read)
    State - u - (read) (NM_DEVICE_STATE)
    Ip4Config - o - (read)
    Dhcp4Config - o - (read)
    Managed - b - (read)
    DeviceType - u - (read)
    
     Enumerated types:
    NM_DEVICE_STATE
    NM_DEVICE_STATE_REASON
    
     Sets of flags:
    NM_DEVICE_CAP
    """
    class State(Enum):
        UNKNOWN = 0
        UNMANAGED = 1
        UNAVAILABLE = 2
        DISCONNECTED = 3
        PREPARE = 4
        CONFIG = 5
        NEED_AUTH = 6
        IP_CONFIG = 7
        ACTIVATED = 8
        FAILED = 9

    class StateReason(Enum):
        UNKNOWN = 0
        NONE = 1
        NOW_MANAGED = 2
        NOW_UNMANAGED = 3
        CONFIG_FAILED = 4
        CONFIG_UNAVAILABLE = 5
        CONFIG_EXPIRED = 6
        NO_SECRETS = 7
        SUPPLICANT_DISCONNECT = 8
        SUPPLICANT_CONFIG_FAILED = 9
        SUPPLICANT_FAILED = 10
        SUPPLICANT_TIMEOUT = 11
        PPP_START_FAILED = 12
        PPP_DISCONNECT = 13
        PPP_FAILED = 14
        DHCP_START_FAILED = 15
        DHCP_ERROR = 16
        DHCP_FAILED = 17
        SHARED_START_FAILED = 18
        SHARED_FAILED = 19
        AUTOIP_START_FAILED = 20
        AUTOIP_ERROR = 21
        AUTOIP_FAILED = 22
        MODEM_BUSY = 23
        MODEM_NO_DIAL_TONE = 24
        MODEM_NO_CARRIER = 25
        MODEM_DIAL_TIMEOUT = 26
        MODEM_DIAL_FAILED = 27
        MODEM_INIT_FAILED = 28
        GSM_APN_FAILED = 29
        GSM_REGISTRATION_NOT_SEARCHING = 30
        GSM_REGISTRATION_DENIED = 31
        GSM_REGISTRATION_TIMEOUT = 32
        GSM_REGISTRATION_FAILED = 33
        GSM_PIN_CHECK_FAILED = 34
        FIRMWARE_MISSING = 35
        REMOVED = 36
        SLEEPING = 37
        CONNECTION_REMOVED = 38
        USER_REQUESTED = 39
        CARRIER = 40

    class DeviceType(Enum):
        UNKNOWN = 0
        ETHERNET = 1
        WIRELESS = 2
        GSM = 3
        CDMA = 4

    class Cap(Flags):
        NONE = 0x0
        NM_SUPPORTED = 0x1
        CARRIER_DETECT = 0x2

    @classmethod
    def _settings_type(cls):
        """The matching settings["connection"]["type"]"""
        AbstractMethodCalled    # no standard way for saying 'abstract'

    DBusClient._add_adaptors({
        "signals": {
            "StateChanged": (identity, [State, State, StateReason], {})
            },
        "properties": {
            "Capabilities": Cap,
            "Ip4Address": Ip4Address,
            "State": State,
            "Ip4Config": Ip4Config,
            "Dhcp4Config": Dhcp4Config,
            "Managed": bool,
            "DeviceType": DeviceType,
            },
        })

    SERVICE = "org.freedesktop.NetworkManager"
    IFACE = "org.freedesktop.NetworkManager.Device"

    def __init__(self, opath):
        """Inits the base class, unlike _create"""
        super(Device, self).__init__(dbus.SystemBus(), self.SERVICE, opath, default_interface = self.IFACE)


    _constructors = {}
    @staticmethod
    def _register_constructor(type, ctor):
#        print "REGISTERING", type, repr(type), ctor
        Device._constructors[type] = ctor

    @staticmethod
    def _create(opath):
        base = Device(opath)       # Class
        type = base["DeviceType"] # _type()
#        print "TYPE", type, repr(type)
        try:
            ctor = Device._constructors[int(type)] # TODO int is not nice
#            print "CONSTRUCTING:", ctor
            return ctor(opath)
        except KeyError, e:
#            print repr(e)
            return base

        
#    def __str__(self):
# FIXME how to override str?
#    def __repr__(self):
#        return "DEVICE " + self.object_path

# FIXME make them separate to enable plugins
class Wired(Device):
    "TODO docstring, move them to the class"

    @classmethod
    def _settings_type(cls):
        return "802-3-ethernet"

    # FIXME but also use parent iface
    IFACE = "org.freedesktop.NetworkManager.Device"
    # FIXME how to get parent adaptors?
    DBusClient._add_adaptors({
            "signals": {
                "PropertiesChanged": (identity, [identity], {})
                },
            "properties": {
#                "HwAddress": identity,
#                "Speed": identity,
                "Carrier": bool,
                },
            })

Device._register_constructor(Device.DeviceType.ETHERNET, Wired)


class Wireless(Device):

    class DeviceCap(Flags):
        NONE = 0x0
        CIPHER_WEP40 = 0x1
        CIPHER_WEP104 = 0x2
        CIPHER_TKIP = 0x4
        CIPHER_CCMP = 0x8
        WPA = 0x10
        RSN = 0x20

    @classmethod
    def _settings_type(cls):
        return "802-11-wireless"

    DBusClient._add_adaptors({
        "methods": {
            "GetAccessPoints": seq_adaptor(AccessPoint),
            },
        "signals": {
            "PropertiesChanged": (identity, [identity], {}),
            "AccessPointAdded": (identity, [AccessPoint], {}),
            "AccessPointRemoved": (identity, [AccessPoint], {}),
            },
        "properties": {
            "Mode": Mode,
            "ActiveAccessPoint": AccessPoint,
            "WirelessCapabilities": DeviceCap,
            },
        })

Device._register_constructor(Device.DeviceType.WIRELESS, Wireless)
