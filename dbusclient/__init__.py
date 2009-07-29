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
        pmi = dbus.Interface(self, "org.freedesktop.DBus.Properties")
        return pmi.Set(iface, key, value)

def mklist(x):
    if isinstance(x, list):
        return x
    elif isinstance(x, tuple):
        return [i for i in x]
    else:
        return [x]

#class DBusClient(dbus.proxies.Interface):
class DBusClient(DBusMio):
    _adaptors = {
        "methods": {},
        "signals": {},
        "properties": {},
        }

    
    @classmethod
    def _get_adaptor(cls, kind, name):
#        print "GET", cls, kind, name
        try:
            return cls._adaptors[kind][name]
        except KeyError:
            scls = cls.__mro__[1] # can use "super"? how?
            try:
                return scls._get_adaptor(kind, name)
            except AttributeError: # no _get_adaptor there
                raise KeyError(":".join((kind, name)))

    @classmethod
    def _add_adaptor(cls, kind, name, adaptor):
#        print "ADD", cls, kind, name, adaptor
        adaptor = mklist(adaptor)
        try:
            args = adaptor[1]
        except:
            args = []
        args = mklist(args)
        try:
            kwargs = adaptor[2]
        except:
            kwargs = {}
        cls._adaptors[kind][name] = [adaptor[0], args, kwargs]
            

    @classmethod
    def _add_adaptors(cls, *args, **kwargs):
        """
        either 
        """
        if not cls.__dict__.has_key("_adaptors"):
            # do not use inherited attribute
            cls._adaptors = {"methods":{}, "properties":{}, "signals":{}}
        if len(args) != 0:
            assert len(kwargs) == 0
            assert len(args) == 1
            kwargs = args[0]

        for section in cls._adaptors.keys():
            secsource = kwargs.pop(section, {})
            for name, adaptor in secsource.iteritems():
                cls._add_adaptor(section, name, adaptor)
        assert len(kwargs) == 0
#        print "AA", cls, cls._adaptors

    def __getattr__(self, name):
        "Wrap return values"

        callable = super(DBusClient, self).__getattr__(name)
        try:
            adaptor = self._get_adaptor("methods", name)
            return async_callable_universal_adaptor(callable, adaptor)
        except KeyError:
            return callable

    # properties
    def __getitem__(self, key):
        value = super(DBusClient, self).__getitem__(key)
        try:
            adaptor = self._get_adaptor("properties", key)[0]
        except KeyError, IndexError:
            adaptor = identity
        return adaptor(value)

    def __setitem__(self, key, value):
        try:
            adaptor = self._get_adaptor("properties", key)[1][0]
        except KeyError, IndexError:
            adaptor = identity
        value = adaptor(value)
        return super(DBusClient, self).__setitem__(key, value)


    # signals
    # overrides a ProxyObject method
    def _connect_to_signal(self, signame, handler, interface=None, **kwargs):
        "Wrap signal handler, with arg adaptors"

        # TODO also demarshal kwargs
        adaptor = self._get_adaptor("signals", signame)
        wrap_handler = callable_universal_adaptor(handler, adaptor)
        return self.connect_to_signal(signame, wrap_handler, interface, **kwargs)

#class ObjectAddress:
#    """An object path, optionally with a service/connection where to find it"""
#    pass
