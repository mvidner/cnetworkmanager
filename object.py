import dbus

NMC = 'org.freedesktop.NetworkManager'
PI = 'org.freedesktop.DBus.Properties'

class cObject:
    def __init__(self, opath, svc=NMC):
        self.bus = dbus.SystemBus()
        self.opath = opath
        self.svc = svc
        self.obj = self.bus.get_object(self.svc, self.opath)
        self.pi = dbus.Interface(self.obj, dbus_interface=PI)

    def get_property(self, iface, property_name):
        return self.pi.Get(iface, property_name)

    def set_property(self, iface, property_name, value):
        return self.pi.Set(iface, property_name, value)
