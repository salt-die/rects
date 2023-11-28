from rects import Rect, Region
from rects.region import Band


def test_disjoint_subtraction():
    a = Region.from_rect(Rect(0, 0, 10, 10))
    b = Region.from_rect(Rect(0, 15, 10, 10))
    assert a - b == a


def test_vertical_subtraction():
    a = Region.from_rect(Rect(0, 0, 10, 10))
    b = Region.from_rect(Rect(0, 5, 10, 10))
    assert a - b == Region([Band(0, 5, [0, 10])])


def test_horizontal_subtraction():
    a = Region.from_rect(Rect(0, 0, 10, 10))
    b = Region.from_rect(Rect(5, 0, 10, 10))
    assert a - b == Region([Band(0, 10, [0, 5])])


def test_offset_subtraction():
    a = Region.from_rect(Rect(0, 0, 10, 10))
    b = Region.from_rect(Rect(5, 5, 10, 10))
    assert a - b == Region([Band(0, 5, [0, 10]), Band(5, 10, [0, 5])])
