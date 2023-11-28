from rects import Rect, Region
from rects.region import Band


def test_disjoint_xor():
    a = Region.from_rect(Rect(0, 0, 10, 10))
    b = Region.from_rect(Rect(0, 15, 10, 10))
    assert a ^ b == Region([Band(0, 10, [0, 10]), Band(15, 25, [0, 10])])


def test_vertical_xor():
    a = Region.from_rect(Rect(0, 0, 10, 10))
    b = Region.from_rect(Rect(0, 5, 10, 10))
    assert a ^ b == Region([Band(0, 5, [0, 10]), Band(10, 15, [0, 10])])


def test_horizontal_xor():
    a = Region.from_rect(Rect(0, 0, 10, 10))
    b = Region.from_rect(Rect(5, 0, 10, 10))
    assert a ^ b == Region([Band(0, 10, [0, 5, 10, 15])])


def test_offset_xor():
    a = Region.from_rect(Rect(0, 0, 10, 10))
    b = Region.from_rect(Rect(5, 5, 10, 10))
    assert a ^ b == Region(
        [Band(0, 5, [0, 10]), Band(5, 10, [0, 5, 10, 15]), Band(10, 15, [5, 15])]
    )
