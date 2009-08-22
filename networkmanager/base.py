import dbus
from dbusclient import DBusClient

"""The bus where NetworkManager objects live.

It can be globally changed to a debugging bus for a mock NM service.
Having that as a parameter would complicate the API for the normal
use case, so it is factored out here.
"""
NM_BUS = dbus.SystemBus()
#print "Global Bus:", NM_BUS
def Bus():
#    print "Bus:", NM_BUS
    return NM_BUS

class Base(DBusClient):
    def __init__(self, bus_name=None, object_path=None, introspect=True, follow_name_owner_changes=False, **kwargs):
        conn = Bus()
        super(Base, self).__init__(conn, bus_name, object_path, introspect, follow_name_owner_changes, **kwargs)

    
