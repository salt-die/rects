from .band import Band, INF_BAND
from .data_structures import Rect


class Region:
    """
    Collection of mutually exclusive bands.
    """
    def __init__(self):
        self.bands = [ INF_BAND ]

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
