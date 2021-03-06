from .data_structures import Interval, Rect
from .merge import merge


class Band:
    """
    A vertical interval and a list of walls.
    """
    __slots__ = 'topbottom', 'walls'

    def __init__(self, topbottom: Interval, walls: list[int]):
        self.topbottom = topbottom
        self.walls = walls

    @classmethod
    def from_rect(cls, rect: Rect):
        return cls(rect.topbottom, [*rect.leftright])

    @property
    def top(self):
        return self.topbottom.start

    @property
    def bottom(self):
        return self.topbottom.stop

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
    def bounds(self):
        """
        Bounding rect of entire band.
        """
        walls = self.walls
        return Rect(self.topbottom, Interval(walls[0], walls[-1]))

    def __len__(self):
        """
        Number of rects in the band.
        """
        return len(self.walls) // 2

    def __lt__(self, other):
        return self.topbottom < other.topbottom

    def split(self, n: int):
        """
        Split band along the horizontal line at n. Band's topbottom is modified to be the
        upper portion of the split. A new band is returned for the bottom portion of the split.
        """
        top, bottom = self.topbottom
        self.topbottom = Interval(top, n)

        return Band(Interval(n, bottom), self.walls.copy())

    def __or__(self, other):
        """
        Union of two bands.
        """
        return Band(
            self.topbottom,
            merge(self.walls, other.walls, lambda a, b: a or b),
        )

    def __and__(self, other):
        """
        Intersection of two bands.
        """
        return Band(
            self.topbottom,
            merge(self.walls, other.walls, lambda a, b: a and b),
        )

    def __xor__(self, other):
        """
        Xor of two bands.
        """
        return Band(
            self.topbottom,
            merge(self.walls, other.walls, lambda a, b: a ^ b),
        )

    def __sub__(self, other):
        """
        Subtraction of two bands.
        """
        return Band(
            self.topbottom,
            merge(self.walls, other.walls, lambda a, b: a and not b),
        )

    def __repr__(self):
        attrs = ', '.join(
            f'{attr}={getattr(self, attr)}'
            for attr in self.__slots__
        )
        return f'{type(self).__name__}({attrs})'
