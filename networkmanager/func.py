# FIXME do we need to ensure that objects get unique proxies? how?

# TODO object conversions should be more automatic
# TODO distinguish marshallers/demarshallers

def seq_adaptor(item_adaptor):
    return lambda seq: map(item_adaptor, seq)

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

def convert_seq(seq, ocers):
    """Convert seq's items using respective ocer from ocers.

    seq and ocers must have same length."""

    if len(seq) != len(ocers):
        print "SEQ:", seq
        print "OCERS:", ocers
        raise
    return [ocer(obj) for obj, ocer in zip(seq, ocers)]

def convert_dict(dict, ocer_dict):
    """Convert dict's items using respective ocer from ocer_dict.

    ocer_dict must have items for all keys in dict."""
    retval = {}
    for key, value in dict.iteritems():
        ocer = ocer_dict[key]
        retval[key] = ocer(value)
    return retval

def callable_universal_adaptor(callable, adaptor_spec):
    """

    adaptor_spec is (retval_ocer, arg_ocers, kwarg_ocer_dict)"""

#    print "ADAPTORS:", adaptor_spec
    retval_ocer = adaptor_spec[0]
    arg_ocers = adaptor_spec[1]
    kwarg_ocer_dict = adaptor_spec[2]
    l = lambda *args, **kwargs: \
        retval_ocer(
            callable(
                * convert_seq(args, arg_ocers),
                ** convert_dict(kwargs, kwarg_ocer_dict)
                )
            )
    return l

def compose_ocers(outer, inner):
    return lambda x: outer(inner(x))

def identity(x):
    return x

def void(x):
    return None
