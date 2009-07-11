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

    # --- properties ---

    def prop_iface(self):
        raise "abstract"
    # TODO alias as []
    def get_property(self, property_name):
        iface = self.prop_iface()
        return self.pi.Get(iface, property_name)

    def set_property(self, property_name, value):
        iface = self.prop_iface()
        return self.pi.Set(iface, property_name, value)

    def dump_props(self, prop_names, indent="  "):
        for P in prop_names:
            print "%s%s: %s" % (indent, P, self.get_property(P))
