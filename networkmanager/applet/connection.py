# -*- coding: utf-8 -*-

import dbus
from dbusclient import DBusClient
from networkmanager.base import Base
#from dbusclient.func import *


class Connection(Base):
    """NetworkManagerSettings.Connection (including Secrets)

     Methods:
    Update ( a{sa{sv}}: properties ) → nothing
    Delete ( ) → nothing
    GetSettings ( ) → a{sa{sv}}
    GetSecrets ( s: setting_name, as: hints, b: request_new ) → a{sa{sv}}
    
     Signals:
    Updated ( a{sa{sv}}: settings )
    Removed ( )
    """

    IFACE = "org.freedesktop.NetworkManagerSettings.Connection"
    # FIXME
    SECRETS_IFACE = "org.freedesktop.NetworkManagerSettings.Connection.Secrets"

    def __init__(self, service, opath):
        super(Connection, self).__init__(service, opath, default_interface=self.IFACE)

# no adaptors necessary, it seems
Connection._add_adaptors(
    )
