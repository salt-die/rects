from dataclasses import dataclass, field
from operator import and_, or_, xor
from typing import Callable, Iterator, Self


def sub(a: bool, b: bool) -> bool:
    """`a` and not `b`"""
    return a and not b


def _merge(a: list[int], b: list[int], op: Callable[[bool, bool], bool]) -> list[int]:
    """Merge the walls of two bands given a set operation."""
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


@dataclass(slots=True, frozen=True)
class Rect:
    x: int
    y: int
    width: int
    height: int


@dataclass(slots=True)
class Band:
    """A row of mutually exclusive rects."""

    y1: int
    y2: int
    walls: list[int]

    def __post_init__(self):
        if self.y2 <= self.y1:
            raise ValueError(
                f"Band invalid, y1 ({self.y1}) is not smaller than y2 ({self.y2})"
            )


@dataclass(slots=True)
class Region:
    """Collection of mutually exclusive bands of rects."""

    bands: list[Band] = field(default_factory=list)

    def _coalesce(self):
        """Join contiguous bands with the same walls to reduce rects."""
        bands = self.bands = [band for band in self.bands if len(band.walls) > 0]

        i = 0
        while i < len(bands) - 1:
            a, b = bands[i], bands[i + 1]
            if b.y1 <= a.y2 and a.walls == b.walls:
                a.y2 = b.y2
                del bands[i + 1]
            else:
                i += 1

    def _merge_regions(self, other: Self, op: Callable[[bool, bool], bool]) -> Self:
        bands = []
        i = j = 0
        scanline = -float("inf")

        while i < len(self.bands) and j < len(other.bands):
            r, s = self.bands[i], other.bands[j]
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
                    bands.append(Band(scanline, r.y2, _merge(r.walls, [], op)))
                    scanline = r.y2
                    i += 1
                elif r.y2 < s.y2:
                    if scanline < s.y1:
                        ## ---------------
                        ## - - - - - - - - scanline
                        ##        r
                        ##        ~~~~~~~~~~~~~~~
                        ## ---------------
                        ##               s
                        ##        ~~~~~~~~~~~~~~~
                        bands.append(Band(scanline, s.y1, _merge(r.walls, [], op)))
                    if s.y1 < r.y2:
                        ## ---------------
                        ##        r
                        ##        ~-~-~-~-~-~-~-~ scanline
                        ## ---------------
                        ##               s
                        ##        ~~~~~~~~~~~~~~~
                        bands.append(Band(s.y1, r.y2, _merge(r.walls, s.walls, op)))
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
                        bands.append(Band(scanline, s.y1, _merge(r.walls, [], op)))
                    ## ---------------
                    ##        r
                    ##        ~-~-~-~-~-~-~-~ scanline
                    ##               s
                    ##        ~~~~~~~~~~~~~~~
                    ## ---------------
                    bands.append(Band(s.y1, s.y2, _merge(r.walls, s.walls, op)))
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
                    bands.append(Band(scanline, s.y2, _merge([], s.walls, op)))
                    scanline = s.y2
                    j += 1
                elif s.y2 < r.y2:
                    if scanline < r.y1:
                        ## ~~~~~~~~~~~~~~~
                        ## - - - - - - - - scanline
                        ##        s
                        ##        ---------------
                        ## ~~~~~~~~~~~~~~~
                        ##               r
                        ##        ---------------
                        bands.append(Band(scanline, r.y1, _merge([], s.walls, op)))
                    if r.y1 < s.y2:
                        ## ~~~~~~~~~~~~~~~
                        ##        s
                        ##        --------------- scanline
                        ## ~~~~~~~~~~~~~~~
                        ##               r
                        ##        ---------------
                        bands.append(Band(r.y1, s.y2, _merge(r.walls, s.walls, op)))
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
                        bands.append(Band(scanline, r.y1, _merge([], s.walls, op)))
                    ## ~~~~~~~~~~~~~~~
                    ##        s
                    ##        --------------- scanline
                    ##               r
                    ##        ---------------
                    ## ~~~~~~~~~~~~~~~
                    bands.append(Band(r.y1, r.y2, _merge(r.walls, s.walls, op)))
                    scanline = r.y2
                    if r.y2 == s.y2:
                        j += 1
                    i += 1

        while i < len(self.bands):
            r = self.bands[i]
            if scanline < r.y1:
                scanline = r.y1
            bands.append(Band(scanline, r.y2, _merge(r.walls, [], op)))
            i += 1

        while j < len(other.bands):
            s = other.bands[j]
            if scanline < s.y1:
                scanline = s.y1
            bands.append(Band(scanline, s.y2, _merge([], s.walls, op)))
            j += 1

        region = Region(bands=bands)
        region._coalesce()
        return region

    def __and__(self, other: Self) -> Self:
        return self._merge_regions(other, and_)

    def __add__(self, other: Self) -> Self:
        return self._merge_regions(other, or_)

    def __or__(self, other: Self) -> Self:
        return self._merge_regions(other, or_)

    def __sub__(self, other: Self) -> Self:
        return self._merge_regions(other, sub)

    def __xor__(self, other: Self) -> Self:
        return self._merge_regions(other, xor)

    def rects(self) -> Iterator[Rect]:
        """Yield all rects that make up the region."""
        for band in self.bands:
            height = band.y2 - band.y1
            i = 0
            while i < len(band.walls):
                yield Rect(
                    band.walls[i], band.y1, band.walls[i + 1] - band.walls[i], height
                )
                i += 2

    @property
    def bbox(self) -> Rect | None:
        """Bounding box of region or None if region is empty."""
        if not self.bands:
            return

        y = self.bands[0].y1
        x = min(band.walls[0] for band in self.bands)
        height = self.bands[-1].y2 - y
        width = max(band.walls[-1] for band in self.bands) - x

        return Rect(x, y, width, height)

    @classmethod
    def from_rect(cls, rect: Rect) -> Self:
        """Create a region from an initial rect."""
        return cls([Band(rect.y, rect.y + rect.height, [rect.x, rect.x + rect.width])])
