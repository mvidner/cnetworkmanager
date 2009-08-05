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

class Table(object):
    """Formats a table

    >>> t = Table("A", "Bee", "C")

    >>> t.row("ay", "B", "sea")

    >>> t.row("", "b", "c")

    >>> print t
    A  | Bee | C  
    ---+-----+----
    ay | B   | sea
       | b   | c  

    >>> Table.terse = True

    >>> print t
    ay|B|sea
    |b|c
    """
    # there are trailing spaces in the above non-terse printout

    terse = False
    "No headings and no padding, suitable for parsing."

    def __init__(self, *args):
        "The arguments are column headings."

        self.headings = args
        self.rows = []

    def row(self, *args):
        """The arguments are row items.

        str is applied to them"""
        self.rows.append(map(str,args))

    @staticmethod
    def pad_row(row, col_sizes):
        return map(str.ljust, row, col_sizes)

    def col_widths(self):
        "Returns a list of the column widths."

        # the table of lengths of original items
        lengths = map(lambda cells: map(len, cells), self.rows + [self.headings])
        return reduce(lambda cells1, cells2: map(max, cells1, cells2), lengths)

    def terse_str(self):
        "Formats the table, tersely."

        rs = map("|".join, self.rows)
        return "\n".join(rs)

    def __str__(self):
        "Formats the table."

        if self.terse:
            return self.terse_str()

        cw = self.col_widths()
        def fmt_row(items):
            return " | ".join(self.pad_row(items, cw))
        h = fmt_row(self.headings)
        s = "-+-".join(map(lambda w: "-" * w, cw))
        rs = map(fmt_row, self.rows)
        rs.insert(0, s)
        rs.insert(0, h)
        return "\n".join(rs)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
