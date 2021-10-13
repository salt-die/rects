from typing import NamedTuple


class Interval(NamedTuple):
    """
    A continuous interval.
    """
    start: int
    stop: int

    @property
    def measure(self):
        return self.stop - self.start

    def __contains__(self, other: int):
        if not isinstance(other, int):
            return NotImplemented

        return self.start <= other < self.stop

    def intersects(self, other):
        if not isinstance(other, Interval):
            return NotImplemented

        return other.start in self or self.start in other


class Rect(NamedTuple):
    """
    A cross product of two intervals.
    """
    topbottom: Interval
    leftright: Interval

    @property
    def height(self) -> int:
        return self.topbottom.measure

    @property
    def width(self) -> int:
        return self.leftright.measure

    def __contains__(self, point) -> bool:
        """
        Return true if point is contained in the rect.
        """
        py, px = point

        return py in self.topbottom and px in self.leftright

    def intersects(self, other) -> bool:
        """
        Return true if rect intersects with other.
        """
        return (
            self.topbottom.intersects(other.topbottom)
            and self.leftright.intersects(other.leftright)
        )


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


class Region:
    """
    Collection of mutually exclusive bands.
    """
    def __init__(self, *bands):
        self.bands = list(bands)

    def __and__(self, other: Rect):
        raise NotImplementedError()

    def __or__(self, other: Rect):
        raise NotImplementedError()

    def __sub__(self, other: Rect):
        raise NotImplementedError()

    def __xor__(self, other: Rect):
        raise NotImplementedError()
