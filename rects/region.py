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
        top, bottom = rect_band.topbottom

        i = 0
        while i < len(bands):
            band = bands[i]

            if top != band.top and top in band.topbottom:
                bands.insert(i + 1, band.split(top))
            elif bottom != band.top and bottom in band.topbottom:
                bands.insert(i + 1, band.split(bottom))
            elif band.top != top and band.top in rect_band.topbottom:
                rect_bands[-1:] = [rect_band] = [rect_band.split(band.top)]
                top, bottom = rect_band.topbottom
            elif band.bottom != top and band.bottom in rect_band.topbottom:
                rect_bands[-1:] = [rect_band] = [rect_band.split(band.bottom)]
                top, bottom = rect_band.topbottom

            i += 1

        return rect_bands

    def __repr__(self):
        attrs = ', '.join(
            f'{attr}={getattr(self, attr)}'
            for attr in self.__slots__
        )
        return f'{type(self).__name__}({attrs})'
