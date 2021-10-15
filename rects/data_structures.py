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
