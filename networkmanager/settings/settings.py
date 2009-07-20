# -*- coding: utf-8 -*-

import dbus
from ..dbusclient import DBusClient
from connection import Connection
from ..func import *


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
    PROP_IFACE = IFACE

    def __init__(self, service):
        # default_interface because knetworkmanager doesnt provide introspection
        super(NetworkManagerSettings, self).__init__(dbus.SystemBus(), service, self.OPATH, default_interface = self.IFACE)
        # need instance specific adaptors for user/system conn factories
        self._adaptors["methods"]["ListConnections"] = seq_adaptor(self._create_connection)

    def _create_connection(self, opath):
        return Connection(self.bus_name, opath)

    # FIXME better API for this
    DBusClient._add_adaptors({
            "methods": {
                "ListConnections": seq_adaptor(Connection), # overriden?
                },
            "signals": {
                "NewConnection": (identity, [Connection], {}),
                },
            })

