# -*- coding: utf-8 -*-

import dbus
from ..dbusclient import DBusClient
from connection import Connection
from ..func import *


# TODO NMS.System, not in spec

class NetworkManagerSettings(DBusClient):
    """NetworkManagerSettings

    The NM Settings client library

     Methods:
    ListConnections ( ) → ao

     Signals:
    NewConnection ( o: connection )
    """

    # FIXME into DBusCLient ctor
    OPATH = "/org/freedesktop/NetworkManagerSettings"
    IFACE = "org.freedesktop.NetworkManagerSettings"

    def __init__(self, service):
        # default_interface because knetworkmanager doesnt provide introspection
        super(NetworkManagerSettings, self).__init__(dbus.SystemBus(), service, self.OPATH, default_interface = self.IFACE)
        # need instance specific adaptors for user/system conn factories
        self._add_adaptor("methods", "ListConnections", seq_adaptor(self._create_connection))

    def _create_connection(self, opath):
        return Connection(self.bus_name, opath)

NetworkManagerSettings._add_adaptors(
            signals = {
                "NewConnection": [void, [Connection]],
                },
            )
