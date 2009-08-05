class NamedNumbers(object):
    """Base for Enum and Flags."""

    def __init__(self, value):
        self.value = value
    def __int__(self):
        """
        >>> n = NamedNumbers(42)

        >>> int(n)
        42
        """
        return self.value

class Enum(NamedNumbers):
    """Enumeration."""

    def __str__(self):
        """
        >>> class Foo(Enum):
        ...    ONE = 1
        ...    TWO = 2

        >>> Foo.ONE
        1

        >>> str(Foo(Foo.TWO))
        'TWO'

        >>> str(Foo(3))
        '3'
        """

        for n, v in self.__class__.__dict__.iteritems():
            if v == self.value:
                return n
        return str(self.value)
    # TODO __repr__

class Flags(NamedNumbers):
    """Bit flags."""

    def __str__(self):
        """
        >>> class MyFlags(Flags):
        ...     NONE = 0x0
        ...     EXECUTE = 0x1
        ...     WRITE = 0x2
        ...     READ = 0x4
    
        >>> str(MyFlags(5))
        'EXECUTE,READ'
    
        >>> str(MyFlags(0))
        'NONE'
    
        >>> str(MyFlags(9)) # doctest: +SKIP
        'EXECUTE,0x8'    
        """

        has = {}
        for n, v in self.__class__.__dict__.iteritems():
            if isinstance(v, int): # FIXME long
                if self.value & v or (self.value == 0 and v == 0):
                    has[v] = n
                    
        names = [has[v] for v in sorted(has.keys())]
        # TODO unknown values?
        return ",".join(names)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
