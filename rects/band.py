from textwrap import dedent
from typing import NamedTuple

from .data_structures import Interval, Rect
from .merge import merge

def _operation_factory(symbol, docstring):
    """
    Produces one of the set methods for a Band.

    `exec` is used instead of a passed in function to reduce function calls.
    """
    code = f"""
        def op(self, other):
            assert self.topbottom == other.topbottom

            new_walls = [ ]
            inside_region = False
            for threshold, inside_self, inside_other in merge(self.walls, other.walls):
                if (inside_self {symbol} inside_other) != inside_region:
                    new_walls.append(threshold)
                    inside_region ^= True

            return Band(self.topbottom, new_walls)
    """
    exec(dedent(code), globals(), loc := { })
    loc['op'].__doc__ = docstring
    return loc['op']


class Band(NamedTuple):
    """
    A vertical interval and a list of walls.
    """
    topbottom: Interval
    walls: list[int]

    @property
    def rects(self):
        """
        Yield the Rects that make up the band.
        """
        topbottom = self.topbottom

        it = iter(self.walls)
        for left, right in zip(it, it):
            yield Rect(topbottom, Interval(left, right))

    @property
    def extents(self):
        """
        Bounding rect of entire band.
        """
        return Rect(self.topbottom, Interval(walls[0], walls[-1]))

    def __len__(self):
        """
        Number of rects in the band.
        """
        return len(self.walls) // 2

    def __lt__(self, other):
        if not isinstance(other, Band):
            return NotImplemented

        return self.topbottom < other.topbottom

    def split(self, n: int):
        """
        Split band along the horizontal line at n.
        """
        top, bottom = self.topbottom
        self.topbottom = Interval(top, n)

        return self, Band(Interval(n, bottom), self.walls.copy())

    __or__ = _operation_factory('or', 'Union of two bands.')
    __and__ = _operation_factory('and', 'Intersection of two bands.')
    __xor__ = _operation_factory('^', 'Xor of two bands.')
    __sub__ = _operation_factory('and not', 'Xor of two bands.')
