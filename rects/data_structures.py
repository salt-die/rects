from typing import NamedTuple


class Interval(NamedTuple):
    """
    A continuous interval.
    """
    start: int
    stop: int

    @property
    def length(self):
        return self.stop - self.start

    def __contains__(self, other: int):
        return self.start <= other < self.stop

    def intersects(self, other):
        """
        Return true if two intervals intersect.
        """
        return other.start in self or self.start in other

    def joins(self, other):
        """
        Return true if union of two intervals is a single interval.
        """
        return (
            self.intersects(other)
            or other.end == self.start
            or self.end == other.start
        )


class Rect(NamedTuple):
    """
    A cross product of two intervals.
    """
    topbottom: Interval
    leftright: Interval

    @property
    def height(self) -> int:
        return self.topbottom.length

    @property
    def width(self) -> int:
        return self.leftright.length

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
