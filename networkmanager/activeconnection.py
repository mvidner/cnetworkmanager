# -*- coding: utf-8 -*-

import dbus
from dbusclient import DBusClient, object_path
from dbusclient.func import *
from applet import Connection
from device import Device
from accesspoint import AccessPoint
from base import Base
from util import Enum

class ActiveConnection(Base):
    """
     Signals:
    PropertiesChanged ( a{sv}: properties )
    
     Properties:
    ServiceName - s - (read)
    Connection - o - (read)
    SpecificObject - o - (read)
    Devices - ao - (read)
    State - u - (read) (NM_ACTIVE_CONNECTION_STATE)
    Default - b - (read)
    
     Enumerated types:
    NM_ACTIVE_CONNECTION_STATE
    """

    SERVICE = "org.freedesktop.NetworkManager"
    IFACE = "org.freedesktop.NetworkManager.Connection.Active"

    def __init__(self, opath):
        super(ActiveConnection, self).__init__(self.SERVICE, opath, default_interface=self.IFACE)

    class State(Enum):
        UNKNOWN = 0
        ACTIVATING = 1
        ACTIVATED = 2

    def __getitem__(self, key):
        "Implement Connection by adding the required ServiceName"

        v = super(ActiveConnection, self).__getitem__(key)
        if key == "Connection":
            sn = self.__getitem__("ServiceName")
            v = Connection(sn, v)
        return v

ActiveConnection._add_adaptors(
    PropertiesChanged = SA(identity),
#    ServiceName = PA(identity),
#    Connection = PA(Connection), # implemented in __getitem__
    SpecificObject = PA(AccessPoint), #in most cases. figure out.
    Devices = PA(seq_adaptor(Device._create)),
    State = PA(ActiveConnection.State),
    Default = PA(bool),
    )
