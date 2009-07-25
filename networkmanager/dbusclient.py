import dbus
import functools
from func import *

def object_path(o):
    if isinstance(o, dbus.proxies.ProxyObject):
        return o.object_path
    # hope it is ok
    return o

class DBusMio(dbus.proxies.ProxyObject):
    """Multi-interface object

    BUGS: 1st method call will block with introspection"""

    def __init__(self, conn=None, bus_name=None, object_path=None, introspect=True, follow_name_owner_changes=False, **kwargs):
        # FIXME common for this class, all classes?
        self.__default_interface = kwargs.pop("default_interface", None)
        super(DBusMio, self).__init__(conn, bus_name, object_path, introspect, follow_name_owner_changes, **kwargs)

    def __getattr__(self, name):
        # TODO cache
#        iface = self._interface_cache.get(name)
 #       if iface == None:
        iface = self.__default_interface
        # _introspect_method_map comes from ProxyObject
        # But it will be empty until the async introspection finishes
        self._introspect_block() # FIXME makeit work with async methods
        methods = self._introspect_method_map.keys()
        for im in methods:
            (i, m) = im.rsplit(".", 1)
            if m == name:
                iface = i
#        print "METHOD %s INTERFACE %s" %(name, iface)
        callable = super(DBusMio, self).__getattr__(name)
        return functools.partial(callable, dbus_interface=iface)

    # properties
    def __getitem__(self, key):
        iface = self.__default_interface # TODO cache
        # TODO _introspect_property_map
        pmi = dbus.Interface(self, "org.freedesktop.DBus.Properties")
        return pmi.Get(iface, key)

    def __setitem__(self, key, value):
        iface = self.__default_interface # TODO cache
        # TODO _introspect_property_map
        pmi = dbus.Interface(self._obj, "org.freedesktop.DBus.Properties")
        return pmi.Set(iface, key, value)


#class DBusClient(dbus.proxies.Interface):
class DBusClient(DBusMio):
    _adaptors = {
        "methods": {},
        "signals": {},
        "properties": {},
        }

    # FIXME all mashed together?!
    @staticmethod
    def _add_adaptors(adict):
        target = DBusClient._adaptors
        for section in target.keys():
            target[section].update(adict.get(section, {}))

    def __getattr__(self, name):
        "Wrap return values"

        callable = super(DBusClient, self).__getattr__(name)
        try:
            adaptor = self._adaptors["methods"][name]
        except KeyError:
            adaptor = identity

        if isinstance(adaptor, tuple):
            return callable_universal_adaptor(callable, adaptor)
        return callable_adaptor(callable, adaptor)

    # properties
    def __getitem__(self, key):
        value = super(DBusClient, self).__getitem__(key)
        try:
            adaptor = self._adaptors["properties"][key]
        except KeyError:
            adaptor = identity
        return adaptor(value)

#    def __setitem__(self, key,value):
#        TODO

    # signals
    def _connect_to_signal(self, signame, handler, interface=None, **kwargs):
        "Wrap signal handler, with arg adaptors"

        # TODO also demarshal kwargs
        wrap_handler = callable_universal_adaptor(handler, self._adaptors["signals"][signame])
        return self.connect_to_signal(signame, wrap_handler, interface, **kwargs)

#class ObjectAddress:
#    """An object path, optionally with a service/connection where to find it"""
#    pass
