"""Module with useful classes and functions."""

import operator
from collections import namedtuple, defaultdict


class xytuple(namedtuple("xytuple",("x","y"))):
    """Tuple for x,y coordinates and their transformations.

    This class supports the following operators:
    - addition and inplace addition (+, +=)
    - substraction and inplace substraction (-, -=)
    - multiplication and inplace multiplication (*, *=)
    - division and inplace division (/, /=)

    These are all term-to-term operations.
    Hence, the argument has two be a two-elements iterable.
    They all return an xytuple.

    Also, the absolute value operation is supported (abs).
    It returned a float corrsponding to the norm of the coordinates.

    To apply a specific function on both coordinates, use the method map.
    It returns an xytuple.
    """
    
    __add__ = __iadd__ = lambda self, it: xytuple(*map(operator.add, self, it))
    __add__.__doc__ = """Add a 2-elements iterable and return an xytuple.
                      """
    __sub__ = __isub__ = lambda self, it: xytuple(*map(operator.sub, self, it))
    __sub__.__doc__ = """Substract a 2-elements iterable and return an xytuple.
                      """
    __mul__ = __imul__ = lambda self, it: xytuple(*map(operator.mul, self, it))
    __mul__.__doc__ = """Product by a 2-elements iterable and return an xytuple.
                      """
    __div__ = __idiv__ = lambda self, it: xytuple(*map(operator.div, self, it))
    __div__.__doc__ = """Divide by a 2-elements iterable and return an xytuple.
                      """
    __neg__ = lambda self: self * (-1,-1)
    __neg__.__doc__ = """Return the additive inverse of an xytuple.
                      """
    __abs__ = lambda self: abs(complex(*self))
    __abs__.__doc__ = """Return a float, the norm of the coordinates.
                      """

    def map(self, func):
        """Map the coordinates with the given function a return an xytuple."""
        return xytuple(*map(func, self))


class cursoredlist(list):
    """Enhanced list with a cursor attribute"""
    
    def __init__(self, iterator, cursor=0):
        """Inititalize the cursor.

        :param iterator: Iterator to build the list from
        :type iterator: any iterable
        :param pos: Initial cursor value (default is 0)
        :type pos: int
        """
        list.__init__(self, iterator)
        self.cursor = cursor

    def get(self, default=None):
        """Get the current object."""
        if len(self):
            self.cursor %= len(self)
        try:
            return self[self.cursor]
        except IndexError:
            return default
        
    def inc(self, inc):
        """Increment the cursor and return the new current object.

        :param inc: Number of incrementation of the cursor
        :type inc: int
        """
        self.cursor += inc
        return self.get()

    def dec(self, dec):
        """Decrement the cursor and return the new current object.

        :param dec: Number of decrementation of the cursor
        :type dec: int
        """
        self.cursor -= dec
        return self.get()


class cachedict(defaultdict):

    def __missing__(self, key):
        if isinstance(key, tuple):
            self[key] = self.default_factory(*key)
        else:
            self[key] = self.default_factory(index)
        return self[key]
        
