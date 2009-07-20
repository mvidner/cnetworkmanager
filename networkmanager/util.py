class NamedNumbers:
    def __init__(self, value):
        self.value = value
    def __int__(self):
        return self.value

class Enum(NamedNumbers):
    """enum

    class Foo(Enum):
        FOO=1
        BAR=2

    >>> e = Foo(Foo.BAR)
    >>> str(e)
    "BAR"
    """
    def __str__(self):
        for n, v in self.__class__.__dict__.iteritems():
            if v == self.value:
                return n
        return "?"
    # TODO __repr__

class Flags(NamedNumbers):
    def __str__(self):
        has = {}
        for n, v in self.__class__.__dict__.iteritems():
            if isinstance(v, int) and self.value & v: # FIXME long
                has[v] = n
        names = [has[v] for v in sorted(has.keys())]
        # TODO zero is a special case
        # TODO unknown values?
        return ",".join(names)
