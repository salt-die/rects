from rects import Rect, Region
from rects.region import Band


def test_disjoint_intersection():
    a = Region.from_rect(Rect(0, 0, 10, 10))
    b = Region.from_rect(Rect(0, 15, 10, 10))
    assert a & b == Region([])


def test_vertical_intersection():
    a = Region.from_rect(Rect(0, 0, 10, 10))
    b = Region.from_rect(Rect(0, 5, 10, 10))
    assert a & b == Region([Band(5, 10, [0, 10])])


def test_horizontal_intersection():
    a = Region.from_rect(Rect(0, 0, 10, 10))
    b = Region.from_rect(Rect(5, 0, 10, 10))
    assert a & b == Region([Band(0, 10, [5, 10])])


def test_offset_intersection():
    a = Region.from_rect(Rect(0, 0, 10, 10))
    b = Region.from_rect(Rect(5, 5, 10, 10))
    assert a & b == Region([Band(5, 10, [5, 10])])
