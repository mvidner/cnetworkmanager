# TODO! understand functools
# FIXME do we need to ensure that objects get unique proxies? how?

# TODO object conversions should be more automatic
# TODO distinguish marshallers/demarshallers

def seq_adaptor(item_adaptor):
    return lambda seq: map(item_adaptor, seq)

def callable_adaptor(callable, value_adaptor):
    return lambda *args, **kwargs: value_adaptor(callable(*args, **kwargs))


def callable_args_demarshaller(callable, demarshaller):
    l = lambda *args, **kwargs: callable(* map(demarshaller, args), **kwargs)


# glossary:
#   ocer: object converter. a function taking one object and returning on object
def convert_seq(seq, ocers):
    """Convert seq's items using respective ocer from ocers.

    seq and ocers must have same length."""

    assert(len(seq) == len(ocers)) # FIXME exception instead
#    print "SEQ:", seq
#    print "OCERS:", ocers
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

