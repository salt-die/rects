from rects import Rect, Region
from rects.region import Band


def test_disjoint_xor():
    a = Region.from_rect(Rect(0, 0, 10, 10))
    b = Region.from_rect(Rect(0, 15, 10, 10))
    result = Region([Band(0, 10, [0, 10]), Band(15, 25, [0, 10])])
    assert a ^ b == result
    assert list(result.rects()) == [Rect(0, 0, 10, 10), Rect(0, 15, 10, 10)]
    assert result.bbox == Rect(0, 0, 10, 25)


def test_vertical_xor():
    a = Region.from_rect(Rect(0, 0, 10, 10))
    b = Region.from_rect(Rect(0, 5, 10, 10))
    result = Region([Band(0, 5, [0, 10]), Band(10, 15, [0, 10])])
    assert a ^ b == result
    assert list(result.rects()) == [Rect(0, 0, 10, 5), Rect(0, 10, 10, 5)]
    assert result.bbox == Rect(0, 0, 10, 15)


def test_horizontal_xor():
    a = Region.from_rect(Rect(0, 0, 10, 10))
    b = Region.from_rect(Rect(5, 0, 10, 10))
    result = Region([Band(0, 10, [0, 5, 10, 15])])
    assert a ^ b == result
    assert list(result.rects()) == [Rect(0, 0, 5, 10), Rect(10, 0, 5, 10)]
    assert result.bbox == Rect(0, 0, 15, 10)


def test_offset_xor():
    a = Region.from_rect(Rect(0, 0, 10, 10))
    b = Region.from_rect(Rect(5, 5, 10, 10))
    result = Region(
        [Band(0, 5, [0, 10]), Band(5, 10, [0, 5, 10, 15]), Band(10, 15, [5, 15])]
    )
    assert a ^ b == result
    assert list(result.rects()) == [
        Rect(0, 0, 10, 5),
        Rect(0, 5, 5, 5),
        Rect(10, 5, 5, 5),
        Rect(5, 10, 10, 5),
    ]
    assert result.bbox == Rect(0, 0, 15, 15)


def test_xor_branching_1():
    a = Region([Band(0, 10, [0, 10]), Band(20, 50, [0, 10])])
    b = Region([Band(5, 25, [5, 15]), Band(35, 45, [5, 15])])
    result = Region(
        [
            Band(0, 5, [0, 10]),
            Band(5, 10, [0, 5, 10, 15]),
            Band(10, 20, [5, 15]),
            Band(20, 25, [0, 5, 10, 15]),
            Band(25, 35, [0, 10]),
            Band(35, 45, [0, 5, 10, 15]),
            Band(45, 50, [0, 10]),
        ]
    )
    assert a ^ b == result
    assert list(result.rects()) == [
        Rect(0, 0, 10, 5),
        Rect(0, 5, 5, 5),
        Rect(10, 5, 5, 5),
        Rect(5, 10, 10, 10),
        Rect(0, 20, 5, 5),
        Rect(10, 20, 5, 5),
        Rect(0, 25, 10, 10),
        Rect(0, 35, 5, 10),
        Rect(10, 35, 5, 10),
        Rect(0, 45, 10, 5),
    ]
    assert result.bbox == Rect(0, 0, 15, 50)


def test_xor_branching_2():
    a = Region([Band(0, 10, [0, 10]), Band(40, 50, [0, 10])])
    b = Region([Band(20, 30, [0, 10])])
    result = Region(
        [Band(0, 10, [0, 10]), Band(20, 30, [0, 10]), Band(40, 50, [0, 10])]
    )
    assert a ^ b == result
    assert list(result.rects()) == [
        Rect(0, 0, 10, 10),
        Rect(0, 20, 10, 10),
        Rect(0, 40, 10, 10),
    ]
    assert result.bbox == Rect(0, 0, 10, 50)


def test_xor_branching_3():
    a = Region([Band(0, 10, [0, 10]), Band(15, 25, [0, 10])])
    b = Region([Band(5, 25, [5, 15])])
    result = Region(
        [
            Band(0, 5, [0, 10]),
            Band(5, 10, [0, 5, 10, 15]),
            Band(10, 15, [5, 15]),
            Band(15, 25, [0, 5, 10, 15]),
        ]
    )
    assert a ^ b == result
    assert list(result.rects()) == [
        Rect(0, 0, 10, 5),
        Rect(0, 5, 5, 5),
        Rect(10, 5, 5, 5),
        Rect(5, 10, 10, 5),
        Rect(0, 15, 5, 10),
        Rect(10, 15, 5, 10),
    ]
    assert result.bbox == Rect(0, 0, 15, 25)
