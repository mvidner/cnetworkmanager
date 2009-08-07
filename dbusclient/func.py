"Converters and adaptors."
# TODO check spelling

# TODO object conversions should be more automatic

def seq_adaptor(item_converter):
    "Returns a converter for a sequence, given a converter for one item."
    return lambda seq: map(item_converter, seq)

def identity(x):
    """Identity converter.

    identity(x) == x"""
    return x

def void(x):
    """Dummy converter for functions that return nothing.

    void(x) == None"""
    return None

# random unused ideas about naming all this
"""
raw value, cooked value (RV, CV)

basic operations:
wrap(RV), unwrap(CV) like marshall(CV), demarshall(RV)

proxy: combines both directions
censor, censorer: knows how to both unwrap and wrap
(but does not do both at a time, unlike the real one)
translator

pretty, ugly -> masker
"""

def compose_converters(outer, inner):
    """Converter composition.

    compose_converters(f, g)(x) == f(g(x))"""
    return lambda x: outer(inner(x))

class Adaptor(object):
    """
    An B{adaptor} groups converters for a method, property, or signal.
    (and knows how to apply them?)

    A B{converter} works on values, typically method arguments and return values.
    It takes one value and returns one value (or None, for C{void}).
    
    A B{biconverter} (not implemented) groups two converters that convert
    between two types, such as escaper+unescaper, marshaller+unmarshaller,
    opath_to_object+object_to_opath.    
    """
    __docformat__ = "epytext en"
    def __init__(self, ret, args, kwargs):
        self.ret = ret
        self.args = args
        self.kwargs = kwargs

class CallableAdaptor(Adaptor):
    "Internal, adapts arguments only"

    def __init__(self, *args): # no kwargs yet
        super(CallableAdaptor, self).__init__(args[0], args[1:], {})
        
    @staticmethod
    def convert_seq(seq, converters):
        """Convert seq's items using respective converter from converters.
    
        seq and converters must have same length."""
    
        if len(seq) != len(converters):
            print "SEQ:", seq
            print "CONVERTERS:", converters
            raise
        return [converter(obj) for obj, converter in zip(seq, converters)]
    
    @staticmethod
    def convert_dict(dict, converter_dict):
        """Convert dict's items using respective converter from converter_dict.
    
        converter_dict must have items for all keys in dict.
        ^ NOT, identity is used otherwise
        """
        retval = {}
        for key, value in dict.iteritems():
            converter = converter_dict.get(key, identity)
            retval[key] = converter(value)
        return retval

    def adapt(self, callable):
        def adapted_callable(*args, **kwargs):
            args = self.convert_seq(args, self.args)
            kwargs = self.convert_dict(kwargs, self.kwargs)
            return callable(*args, **kwargs)
        return adapted_callable

class SyncMethodAdaptor(CallableAdaptor):
    """Adapt a method return value and arguments.

    MethodAdaptor(retval_converter, arg1_converter, ...)
    """
    @classmethod
    def kind(cls):
        return "methods"

    def adapt(self, callable):
        args_adapted_callable = super(SyncMethodAdaptor, self).adapt(callable)
        def adapted_callable(*args, **kwargs):
            return self.ret(args_adapted_callable(*args, **kwargs))
        return adapted_callable

class MethodAdaptor(CallableAdaptor):
    """Adapt a method return value and arguments.

    MethodAdaptor(retval_converter, arg1_converter, ...)
    The method may be asynchronous (indicated by certain kwargs in its call)
    in which case we do not adapt the return value.
    (TODO possible to get the reply callback and adapt *that*?)
    """

    @classmethod
    def kind(cls):
        return "methods"

    @staticmethod
    def _is_async(**kwargs):
        return kwargs.has_key('reply_handler') or \
            kwargs.has_key('error_handler') or \
            kwargs.has_key('ignore_reply')
    
    def adapt(self, callable):
        args_adapted_callable = super(MethodAdaptor, self).adapt(callable)
        def adapted_callable(*args, **kwargs):
            if self._is_async(**kwargs):
                return args_adapted_callable(*args, **kwargs)
            else:
                return self.ret(args_adapted_callable(*args, **kwargs))
        return adapted_callable


class PropertyAdaptor(Adaptor):
    """Adapt a property.

    PropertyAdaptor(get_converter [, set_converter])
    """
    # TODO biconverter as sole arg
    def __init__(self, getter, setter=identity):
        # no setter at all for read only?
        super(PropertyAdaptor, self).__init__(getter, [setter], {})

    @classmethod
    def kind(cls):
        return "properties"

    def adapt(self, value):
        return self.ret(value)

    def adapt_write(self, value):
        return self.args[0](value)

class SignalAdaptor(CallableAdaptor):
    """Adapt a signal.

    SignalAdaptor(arg1_converter, ...)
    """
    def __init__(self, *args): # no kwargs yet
        super(SignalAdaptor, self).__init__(void, *args)

    @classmethod
    def kind(cls):
        return "signals"

#FIXME duplicated in pydoc
MA = MethodAdaptor
PA = PropertyAdaptor
SA = SignalAdaptor
