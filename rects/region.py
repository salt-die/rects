from math import inf

from .band import Band
from .data_structures import Rect, Interval

_EMPTY_BAND = Band(topbottom=Interval(inf, inf), walls=[])


class Region:
    """
    Collection of mutually exclusive bands.
    """
    __slots__ = 'bands',

    def __init__(self, extent: Rect=Rect(Interval(-inf, inf), Interval(-inf, inf))):
        self.bands = [ Band.from_rect(extent) ]

    @classmethod
    def from_bands(cls, bands):
        region = cls()
        region.bands = bands
        region._coalesce()
        return region

    def __and__(self, rect: Rect):
        region = Region.from_bands(
            self._merge(
                self._reband(rect),
                lambda a, b: a & b,
            )
        )

        self._coalesce()

        return region


    def __iand__(self, rect: Rect):
        self.bands = self._merge(
            self._reband(rect),
            lambda a, b: a & b,
        )
        self._coalesce()

        return self

    def __or__(self, rect: Rect):
        region = Region.from_bands(
            self._merge(
                self._reband(rect),
                lambda a, b: a | b,
            )
        )

        self._coalesce()

        return region

    def __ior__(self, rect: Rect):
        self.bands = self._merge(
            self._reband(rect),
            lambda a, b: a | b,
        )
        self._coalesce()

        return self

    def __sub__(self, rect: Rect):
        region = Region.from_bands(
            self._merge(
                self._reband(rect),
                lambda a, b: a - b,
            )
        )

        self._coalesce()

        return region

    def __isub__(self, rect: Rect):
        self.bands = self._merge(
            self._reband(rect),
            lambda a, b: a - b,
        )
        self._coalesce()

        return self

    def __xor__(self, rect: Rect):
        region = Region.from_bands(
            self._merge(
                self._reband(rect),
                lambda a, b: a ^ b,
            )
        )

        self._coalesce()

        return region

    def __ixor__(self, rect: Rect):
        self.bands = self._merge(
            self._reband(rect),
            lambda a, b: a ^ b,
        )
        self._coalesce()

        return self

    def _coalesce(self):
        """
        Join contiguous bands that have identical walls.
        """
        bands = self.bands

        i = 0
        while i < len(bands) - 1:
            a, b = bands[i], bands[i + 1]
            if not a.walls:
                bands.pop(i)
            elif not b.walls:
                bands.pop(i + 1)
            elif a.topbottom.joins(b.topbottom) and a.walls == b.walls:
                a.topbottom = Interval(a.top, b.bottom)
                bands.pop(i + 1)
            else:
                i += 1

    def _reband(self, rect: Rect):
        """
        Adjust band topbottom intervals to accomodate rect and return bands that cover rect.
        """
        bands = self.bands
        rect_bands = [ rect_band ] = [ Band(rect.topbottom, walls=[*rect.leftright]) ]

        i = 0
        while i < len(bands):
            band = bands[i]

            if band.topbottom.in_interior(rect_band.top):
                bands.insert(i + 1, band.split(rect_band.top))
            elif band.topbottom.in_interior(rect_band.bottom):
                bands.insert(i + 1, band.split(rect_band.bottom))
            elif rect_band.topbottom.in_interior(band.top):
                rect_bands.append(rect_band := rect_band.split(band.top))
            elif rect_band.topbottom.in_interior(band.bottom):
                rect_bands.append(rect_band := rect_band.split(band.bottom))
            elif band.top >= rect_band.bottom:
                break

            i += 1

        return rect_bands

    def _merge(self, bands, operation):
        a = iter(self.bands)
        b = iter(bands)

        current_a = next(a, _EMPTY_BAND)
        current_b = next(b, _EMPTY_BAND)

        merged = [ ]

        while current_a is not _EMPTY_BAND or current_b is not _EMPTY_BAND:
            if current_a < current_b:
                merged.append(operation(current_a, _EMPTY_BAND))
                current_a = next(a, _EMPTY_BAND)
            elif current_b < current_a:
                merged.append(operation(current_b, _EMPTY_BAND))
                current_b = next(b, _EMPTY_BAND)
            else:
                merged.append(operation(current_a, current_b))
                current_a = next(a, _EMPTY_BAND)
                current_b = next(b, _EMPTY_BAND)

        return merged

    @property
    def rects(self):
        """
        Yield all rects that make up the region.
        """
        for band in self.bands:
            yield from band.rects

    def __repr__(self):
        attrs = ', '.join(
            f'{attr}={getattr(self, attr)}'
            for attr in self.__slots__
        )
        return f'{type(self).__name__}({attrs})'
