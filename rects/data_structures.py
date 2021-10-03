from typing import NamedTuple


class Size(NamedTuple):
    height: int
    width: int


class Point(NamedTuple):
    y: int
    x: int


class Rect(NamedTuple):
    """
    A rect is a rectangular region specified with a point and a size.
    """
    topleft: Point
    size: Size

    @property
    def height(self) -> int:
        return self.size.height

    @property
    def width(self) -> int:
        return self.size.width

    @property
    def topright(self) -> Point:
        y, x = self.topleft
        _, w = self.size

        return Point(y, x + w)

    @property
    def bottomleft(self) -> Point:
        y, x = self.topleft
        h, _ = self.size

        return Point(y + h, x)

    @property
    def bottomright(self) -> Point:
        y, x = self.topleft
        h, w = self.size

        return Point(y + h, x + w)

    def __contains__(self, point: Point) -> bool:
        """
        Return true if point is contained in the rect.
        """
        py, px = point

        y1, x1 = self.topleft
        y2, x2 = self.bottomright

        return y1 <= py <= y2 and x1 <= px <= x2

    def intersects(self, other) -> bool:
        """
        Return true if rect intersects with other.
        """
        self_top, self_left = self.topleft
        self_bottom, self_right = self.bottomright

        other_top, other_left = other.topleft
        other_bottom, other_right = other.bottomright

        return not (
            self_top >= other_bottom
            or other_top >= self_bottom
            or self_left >= other_right
            or other_left >= self_right
        )


class Band(NamedTuple):
    """
    A band is a horizontal region (with a top/bottom) and a list of walls.
    """
    top: int
    bottom: int
    walls: list[int]

    @property
    def rects(self):
        """
        Yield the Rects that make up the band.
        """
        top = self.top
        height = self.bottom - top

        it = iter(self.walls)
        for x1, x2 in zip(it, it):
            yield Rect(
                Point(top, x1),
                Size(height, x2 - x1),
            )

    def __len__(self):
        """
        Number of rects in the band.
        """
        return len(self.walls) // 2
