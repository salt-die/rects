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
    def height(self):
        return self.size.height

    @property
    def width(self):
        return self.size.width

    @property
    def topright(self):
        y, x = self.topleft
        _, w = self.size

        return Point(y, x + w)

    @property
    def bottomleft(self):
        y, x = self.topleft
        h, _ = self.size

        return Point(y + h, x)

    @property
    def bottomright(self):
        y, x = self.topleft
        h, w = self.size

        return Point(y + h, x + w)

    def __contains__(self, point: Point):
        py, px = point

        y1, x1 = self.topleft
        y2, x2 = self.bottomright

        return y1 <= py <= y2 and x1 <= px <= x2

    # TODO: intersects


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
