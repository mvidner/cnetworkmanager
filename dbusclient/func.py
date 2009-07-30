# FIXME do we need to ensure that objects get unique proxies? how?

# TODO object conversions should be more automatic
# TODO distinguish marshallers/demarshallers

def seq_adaptor(item_adaptor):
    return lambda seq: map(item_adaptor, seq)

def identity(x):
    return x

def void(x):
    return None

# glossary:
#   ocer: object converter. a function taking one object and returning on object

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

def compose_ocers(outer, inner):
    return lambda x: outer(inner(x))

"""
A *converter* works on values, typically method arguments and return values.
It takes one value and returns one value (or None, for *void*).

A *biconverter* (not implemented) groups two converters that convert
between two types, such as escaper+unescaper, marshaller+unmarshaller,
opath_to_object+object_to_opath.

An *adaptor* groups converters for a method, property, or signal,
(and knows how to apply them?)
"""
class Adaptor(object):
    def __init__(self, ret, args, kwargs):
        self.ret = ret
        self.args = args
        self.kwargs = kwargs

class CallableAdaptor(Adaptor):
    "Internal, adapts arguments only"

    def __init__(self, *args): # no kwargs yet
        super(CallableAdaptor, self).__init__(args[0], args[1:], {})
        
    @staticmethod
    def convert_seq(seq, ocers):
        """Convert seq's items using respective ocer from ocers.
    
        seq and ocers must have same length."""
    
        if len(seq) != len(ocers):
            print "SEQ:", seq
            print "OCERS:", ocers
            raise
        return [ocer(obj) for obj, ocer in zip(seq, ocers)]
    
    @staticmethod
    def convert_dict(dict, ocer_dict):
        """Convert dict's items using respective ocer from ocer_dict.
    
        ocer_dict must have items for all keys in dict.
        ^ NOT, identity is used otherwise
        """
        retval = {}
        for key, value in dict.iteritems():
            ocer = ocer_dict.get(key, identity)
            retval[key] = ocer(value)
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

#FIXME duplicated in pydoc
MA = MethodAdaptor
PA = PropertyAdaptor
SA = SignalAdaptor
