"Convenience wrappers around dbus-python"

import dbus
import functools

# TODO rename to adaptors
from func import Adaptor, MethodAdaptor, PropertyAdaptor, SignalAdaptor

def object_path(o):
    """Return the object path of o.

    If o is a proxy object, use its appropriate attribute.
    Otherwise assume that o already is an object path.
    """
    if isinstance(o, dbus.proxies.ProxyObject):
        return o.object_path
    # hope it is ok
    return o

class DBusMio(dbus.proxies.ProxyObject):
    """Multi-interface object.

    Will look into introspection data to find which interface
    to use for a method or a property, obviating the need for
    dbus.proxies.Interface.
    If introspection is not available, provide default_interface
    to the constructor.

    BUGS: 1st method call will block with introspection"""

    def __init__(self, conn=None, bus_name=None, object_path=None, introspect=True, follow_name_owner_changes=False, **kwargs):
        """Constructor.

        kwargs may contain default_interface, to be used
        if introspection does not provide it for a method/property
        """

        # FIXME common for this class, all classes?
        self.__default_interface = kwargs.pop("default_interface", None)
        super(DBusMio, self).__init__(conn, bus_name, object_path, introspect, follow_name_owner_changes, **kwargs)

    def __getattr__(self, name):
        """Proxied DBus methods.

        Uses introspection or default_interface to find the interface.
        """
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
        """Proxies DBus properties as dictionary items.

        a = DBusMio(...)
        p = a["Prop"]

        Uses default_interface (because dbus.proxies.ProxyObject
        does not store introspection data for properties, boo. TODO.)
        """

        iface = self.__default_interface # TODO cache
        # TODO _introspect_property_map
        pmi = dbus.Interface(self, "org.freedesktop.DBus.Properties")
        return pmi.Get(iface, key)

    def __setitem__(self, key, value):
        """Proxies DBus properties as dictionary items.

        a = DBusMio(...)
        a["Prop"] = "Hello"

        Uses default_interface (because dbus.proxies.ProxyObject
        does not store introspection data for properties, boo. TODO.)
        """

        iface = self.__default_interface # TODO cache
        # TODO _introspect_property_map
        pmi = dbus.Interface(self, "org.freedesktop.DBus.Properties")
        return pmi.Set(iface, key, value)

def _mklist(x):
    """Return a list.

    Tuples are made into lists, everything else a singleton list.
    """
    if isinstance(x, list):
        return x
    elif isinstance(x, tuple):
        return [i for i in x]
    else:
        return [x]

class DBusClient(DBusMio):
    """
    """
    _adaptors = {
        "methods": {},
        "signals": {},
        "properties": {},
        }

    
    @classmethod
    def _get_adaptor(cls, kind, name):
#        print "GET", cls, kind, name
        try:
            a = cls._adaptors[kind][name]
#            print ">", a
# TODO cache somehow?
            return a
        except KeyError:
            scls = cls.__mro__[1] # can use "super"? how?
            try:
                return scls._get_adaptor(kind, name)
            except AttributeError: # no _get_adaptor there
                raise KeyError(":".join((kind, name)))

    @classmethod
    def _add_adaptor(cls, kind, name, adaptor):
#        print "ADD", cls, kind, name, adaptor
        if isinstance(adaptor, Adaptor):
            cls._adaptors[kind][name] = adaptor
            return

        # this adjusts the (too) flexible list syntax
        adaptor = _mklist(adaptor)
        ret = adaptor[0]
        try:
            args = adaptor[1]
        except:
            args = []
        args = _mklist(args)
        try:
            kwargs = adaptor[2]
        except:
            kwargs = {}

        if kind == "methods":
            adaptor = MethodAdaptor(ret, *args)
        elif kind == "properties":
            setter = args[0] if len(args) else None
            adaptor = PropertyAdaptor(ret, setter)
        elif kind == "signals":
            adaptor = SignalAdaptor(*args)
        cls._adaptors[kind][name] = adaptor
            

    @classmethod
    def _add_adaptors(cls, *args, **kwargs):
        """
        a nested dictionary of kind:name:adaptor,
        either as kwargs (new) or as a single dict arg (old, newest)
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

    @classmethod
    def _add_adaptors2(cls, **kwargs):
        """kwargs: a *flat* dictionary of name: adaptor"""
        adict = {"methods":{}, "properties":{}, "signals":{}}
        for k, v in kwargs.iteritems():
            if isinstance(v, MethodAdaptor):
                adict["methods"][k] = v
            elif isinstance(v, PropertyAdaptor):
                adict["properties"][k] = v
            elif isinstance(v, SignalAdaptor):
                adict["signals"][k] = v
        cls._add_adaptors(adict)

    def __getattr__(self, name):
        "Wrap return values"

        callable = super(DBusClient, self).__getattr__(name)
        try:
            adaptor = self._get_adaptor("methods", name)
            return adaptor.adapt(callable)
        except KeyError:
            return callable

    # properties
    def __getitem__(self, key):
        value = super(DBusClient, self).__getitem__(key)
        try:
            adaptor = self._get_adaptor("properties", key)
            return adaptor.adapt(value)
        except KeyError:
            return value

    def __setitem__(self, key, value):
        try:
            adaptor = self._get_adaptor("properties", key)
            value = adaptor.adapt_write(value)
        except KeyError:
            pass
        return super(DBusClient, self).__setitem__(key, value)


    # signals
    # overrides a ProxyObject method
    def _connect_to_signal(self, signame, handler, interface=None, **kwargs):
        "Wrap signal handler, with arg adaptors"

        # TODO also demarshal kwargs
        adaptor = self._get_adaptor("signals", signame)
        wrap_handler = adaptor.adapt(handler)
        return self.connect_to_signal(signame, wrap_handler, interface, **kwargs)
