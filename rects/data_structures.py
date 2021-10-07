from typing import NamedTuple


class Interval(NamedTuple):
    start: int
    stop: int

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
    A rect is a cross product of two intervals.
    """
    topbottom: Interval
    leftright: Interval

    @property
    def height(self) -> int:
        top, bottom = self.topbottom
        return bottom - top

    @property
    def width(self) -> int:
        left, right = self.leftright
        return right - left

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
    A band is a horizontal interval and a list of walls.
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

    def __len__(self):
        """
        Number of rects in the band.
        """
        return len(self.walls) // 2

    def __lt__(self, other):
        if not isinstance(other, Band):
            return NotImplemented

        return self.topbottom < other.topbottom
