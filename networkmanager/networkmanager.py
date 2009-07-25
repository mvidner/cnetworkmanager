# -*- coding: utf-8 -*-

import dbus
from dbusclient import DBusClient, object_path
from device import Device
from util import Enum
from func import *

# need better/shorter names? or hide them?
SYSTEM_SERVICE = "org.freedesktop.NetworkManagerSystemSettings"
USER_SERVICE = "org.freedesktop.NetworkManagerUserSettings"

class NetworkManager(DBusClient):
    """networkmanager
    
    The NM client library
    
     Methods:
    GetDevices ( ) → ao
    ActivateConnection ( s: service_name, o: connection, o: device, o: specific_object ) → o
    DeactivateConnection ( o: active_connection ) → nothing
    Sleep ( b: sleep ) → nothing
    
     Signals:
    StateChanged ( u: state )
    PropertiesChanged ( a{sv}: properties )
    DeviceAdded ( o: device_path )
    DeviceRemoved ( o: device_path )
    
     Properties:
    WirelessEnabled - b - (readwrite)
    WirelessHardwareEnabled - b - (read)
    ActiveConnections - ao - (read)
    State - u - (read) (NM_STATE)
    
     Enumerated types:
    NM_STATE
    """

    SERVICE = "org.freedesktop.NetworkManager"
    OPATH = "/org/freedesktop/NetworkManager"
    IFACE = "org.freedesktop.NetworkManager"

    def __init__(self):
        super(NetworkManager, self).__init__(dbus.SystemBus(), self.SERVICE, self.OPATH, default_interface=self.IFACE)


    class State(Enum):
        UNKNOWN = 0
        ASLEEP = 1
        CONNECTING = 2
        CONNECTED = 3
        DISCONNECTED = 4

    "TODO find a good term for 'adaptor'"
    _adaptors = {
        "methods": {
            "GetDevices": seq_adaptor(Device._create),
            "ActivateConnection": (identity, [identity, object_path, object_path, object_path], {}),
            "DeactivateConnection": (identity, [object_path], {})
            },
        "properties": {
            "State": State,
            "WirelessEnabled": bool,
            "WirelessHardwareEnabled": bool,
            "ActiveConnections": seq_adaptor(identity), # TODO
            },
        "signals": {
            "StateChanged": (identity, [State], {}),
            },
        }

