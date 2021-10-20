from math import inf

from .band import Band
from .data_structures import Rect, Interval


class Region:
    """
    Collection of mutually exclusive bands.
    """
    __slots__ = 'bands',

    def __init__(self):
        self.bands: list[Band] = [ Band(Interval(-inf, inf), [-inf, inf]) ]

    def __and__(self, other: Rect):
        raise NotImplementedError()

    def __iand__(self, other: Rect):
        raise NotImplementedError()

    def __or__(self, other: Rect):
        raise NotImplementedError()

    def __ior__(self, other: Rect):
        raise NotImplementedError()

    def __sub__(self, other: Rect):
        raise NotImplementedError()

    def __isub__(self, other: Rect):
        raise NotImplementedError()

    def __xor__(self, other: Rect):
        raise NotImplementedError()

    def __ixor__(self, other: Rect):
        raise NotImplementedError()

    def _coalesce(self):
        """
        Join contiguous bands that have identical walls.
        """

    def _reband(self, rect: Rect):
        """
        Adjust band topbottom intervals to accomodate rect.
        """
        bands = self.bands
        rect_bands = [ rect_band ] = [ Band(rect.topbottom, [*rect.leftright]) ]

        i = 0
        while i < len(bands):
            band = bands[i]

            if band.topbottom.in_interior(rect_band.top):
                bands.insert(i + 1, band.split(rect_band.top))
            elif band.topbottom.in_interior(rect_band.bottom):
                bands.insert(i + 1, band.split(rect_band.bottom))
            elif rect_band.topbottom.in_interior(band.top):
                rect_band = rect_band.split(band.top)
                rect_bands.append(rect_band)
            elif rect_band.topbottom.in_interior(band.bottom):
                rect_band = rect_band.split(band.top)
                rect_bands.append(rect_band)

            i += 1

        return rect_bands

    def __repr__(self):
        attrs = ', '.join(
            f'{attr}={getattr(self, attr)}'
            for attr in self.__slots__
        )
        return f'{type(self).__name__}({attrs})'
