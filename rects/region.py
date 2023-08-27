from dataclasses import dataclass
from operator import or_, and_, xor
from typing import Callable, Iterator

_NO_WALLS = []  # We keep around an empty list to pass to _merge.
BoolOp = Callable[[bool, bool], bool]

def sub(a: bool, b: bool) -> bool:
    """
    `a` and not `b`
    """
    return a and not b

def _merge(op: BoolOp, a: list[int], b: list[int]) -> list[int]:
    """
    Merge the walls of two bands given a set operation.
    """
    i = j = 0
    inside_a = inside_b = inside_region = False
    walls = []

    while i < len(a) or j < len(b):
        current_a = a[i] if i < len(a) else float("inf")
        current_b = b[j] if j < len(b) else float("inf")
        threshold = min(current_a, current_b)

        if current_a == threshold:
            inside_a = not inside_a
            i += 1

        if current_b == threshold:
            inside_b = not inside_b
            j += 1

        if op(inside_a, inside_b) != inside_region:
            inside_region = not inside_region
            walls.append(threshold)

    return walls


@dataclass
class Rect:
    y: int
    x: int
    height: int
    width: int


@dataclass
class Band:
    y1: int
    y2: int
    walls: list[int]

    def __post_init__(self):
        if self.y2 <= self.y1:
            raise ValueError(f"Invalid Band: y1 ({self.y1}) is not smaller than y2 ({self.y2})")


@dataclass
class Region:
    """
    Collection of mutually exclusive bands.
    """
    bands: list[Band]

    @staticmethod
    def _coalesce(bands: list[Band]):
        """
        Join contiguous bands with the same walls to reduce rects.
        """
        i = 0
        while i < len(bands) - 1:
            a, b = bands[i], bands[i + 1]
            if len(a.walls) == 0:
                del bands[i]
            elif len(b.walls) == 0:
                del bands[i + 1]
            elif b.y1 <= a.y2 and a.walls == b.walls:
                a.y2 = b.y2
                del bands[i + 1]
            else:
                i += 1

    @classmethod
    def _merge_regions(cls, op: BoolOp, a: "Region", b: "Region") -> "Region":
        bands = []
        i = j = 0
        scanline = -float("inf")

        while i < len(a.bands) and j < len(b.bands):
            r, s = a.bands[i], b.bands[j]
            if r.y1 <= s.y1:
                if scanline < r.y1:
                    scanline = r.y1
                if r.y2 < s.y1:
                    ## ---------------
                    ## - - - - - - - - scanline
                    ##        r
                    ## ---------------
                    ##        ~~~~~~~~~~~~~~~
                    ##               s
                    ##        ~~~~~~~~~~~~~~~
                    bands.append(Band(scanline, r.y2, _merge(op, r.walls, _NO_WALLS)))
                    scanline = r.y2
                    i += 1
                elif s.y1 <= r.y2 and r.y2 < s.y2:
                    if scanline < s.y1:
                        ## ---------------
                        ## - - - - - - - - scanline
                        ##        r
                        ##        ~~~~~~~~~~~~~~~
                        ## ---------------
                        ##               s
                        ##        ~~~~~~~~~~~~~~~
                        bands.append(Band(scanline, s.y1, _merge(op, r.walls, _NO_WALLS)))
                    if s.y1 < r.y2:
                        ## ---------------
                        ##        r
                        ##        ~-~-~-~-~-~-~-~ scanline
                        ## ---------------
                        ##               s
                        ##        ~~~~~~~~~~~~~~~
                        bands.append(Band(s.y1, r.y2, _merge(op, r.walls, s.walls)))
                    scanline = r.y2
                    i += 1
                else:  # r.y2 >= s.y2
                    if scanline < s.y1:
                        ## ---------------
                        ## - - - - - - - - scanline
                        ##        r
                        ##        ~~~~~~~~~~~~~~~
                        ##               s
                        ##        ~~~~~~~~~~~~~~~
                        ## ---------------
                        bands.append(Band(scanline, s.y1, _merge(op, r.walls, _NO_WALLS)))
                    ## ---------------
                    ##        r
                    ##        ~-~-~-~-~-~-~-~ scanline
                    ##               s
                    ##        ~~~~~~~~~~~~~~~
                    ## ---------------
                    bands.append(Band(s.y1, s.y2, _merge(op, r.walls, s.walls)))
                    scanline = s.y2
                    if s.y2 == r.y2:
                        i += 1
                    j += 1
            else:  # s.y1 < r.y1
                if scanline < s.y1:
                    scanline = s.y1
                if s.y2 < r.y1:
                    ## ~~~~~~~~~~~~~~~
                    ## - - - - - - - - scanline
                    ##        s
                    ## ~~~~~~~~~~~~~~~
                    ##        _______________
                    ##               r
                    ##        _______________
                    bands.append(Band(scanline, s.y2, _merge(op, _NO_WALLS, s.walls)))
                    scanline = s.y2
                    j += 1
                elif r.y1 <= s.y2 and s.y2 < r.y2:
                    if scanline < r.y1:
                        ## ~~~~~~~~~~~~~~~
                        ## - - - - - - - - scanline
                        ##        s
                        ##        ---------------
                        ## ~~~~~~~~~~~~~~~
                        ##               r
                        ##        ---------------
                        bands.append(Band(scanline, r.y1, _merge(op, _NO_WALLS, s.walls)))
                    if r.y1 < s.y2:
                        ## ~~~~~~~~~~~~~~~
                        ##        s
                        ##        --------------- scanline
                        ## ~~~~~~~~~~~~~~~
                        ##               r
                        ##        ---------------
                        bands.append(Band(r.y1, s.y2, _merge(op, r.walls, s.walls)))
                    scanline = s.y2
                    j += 1
                else:  # s.y2 >= r.y2
                    if scanline < r.y1:
                        ## ~~~~~~~~~~~~~~~
                        ## - - - - - - - - scanline
                        ##        s
                        ##        ---------------
                        ##               r
                        ##        ---------------
                        ## ~~~~~~~~~~~~~~~
                        bands.append(Band(scanline, r.y1, _merge(op, _NO_WALLS, s.walls)))
                    ## ~~~~~~~~~~~~~~~
                    ##        s
                    ##        --------------- scanline
                    ##               r
                    ##        ---------------
                    ## ~~~~~~~~~~~~~~~
                    bands.append(Band(r.y1, r.y2, _merge(op, r.walls, s.walls)))
                    scanline = r.y2
                    if r.y2 == s.y2:
                        j += 1
                    i += 1

        while i < len(a.bands):
            r = a.bands[i]
            if scanline < r.y1:
                scanline = r.y1
            bands.append(Band(scanline, r.y2, _merge(op, r.walls, _NO_WALLS)))
            i += 1

        while j < len(b.bands):
            s = b.bands[j]
            if scanline < s.y1:
                scanline = s.y1
            bands.append(Band(scanline, s.y2, _merge(op, _NO_WALLS, s.walls)))
            j += 1

        cls._coalesce(bands)
        return cls(bands)

    @classmethod
    def from_rect(cls, rect: Rect) -> "Region":
        """
        Make a region from a `Rect`.
        """
        return cls([Band(rect.y, rect.y + rect.height, [rect.x, rect.x + rect.width])])

    def __and__(self, other: "Region") -> "Region":
        return Region._merge_regions(and_, self, other)

    def __add__(self, other: "Region") -> "Region":
        return Region._merge_regions(or_, self, other)

    def __sub__(self, other: "Region") -> "Region":
        return Region._merge_regions(sub, self, other)

    def __xor__(self, other: "Region") -> "Region":
        return Region._merge_regions(xor, self, other)

    def rects(self) -> Iterator[Rect]:
        """
        Yield rects that make up the region.
        """
        for band in self.bands:
            height = band.y2 - band.y1
            i = 0
            while i < len(band.walls):
                yield Rect(band.y1, band.walls[i], height, band.walls[i + 1] - band.walls[i])
                i += 2


if __name__ == "__main__":
    r = Region.from_rect(Rect(0, 0, 60, 60))
    s = Region.from_rect(Rect(20, 0, 20, 40))
    t = Region.from_rect(Rect(40, 0, 20, 20))

    assert r == r - s + s - t + t

    print(r - s - t)
    for rect in (r - s - t).rects():
        print(rect)

    try:
        Band(5, 3, [1, 2, 3])
    except ValueError as e:
        print(e)
