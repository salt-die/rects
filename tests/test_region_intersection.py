from rects import Rect, Region
from rects.region import Band


def test_disjoint_intersection():
    a = Region.from_rect(Rect(0, 0, 10, 10))
    b = Region.from_rect(Rect(0, 15, 10, 10))
    result = Region()
    assert a & b == result
    assert list(result.rects()) == []
    assert result.bbox is None


def test_vertical_intersection():
    a = Region.from_rect(Rect(0, 0, 10, 10))
    b = Region.from_rect(Rect(0, 5, 10, 10))
    result = Region([Band(5, 10, [0, 10])])
    assert a & b == result
    assert list(result.rects()) == [Rect(0, 5, 10, 5)]
    assert result.bbox == Rect(0, 5, 10, 5)


def test_horizontal_intersection():
    a = Region.from_rect(Rect(0, 0, 10, 10))
    b = Region.from_rect(Rect(5, 0, 10, 10))
    result = Region([Band(0, 10, [5, 10])])
    assert a & b == result
    assert list(result.rects()) == [Rect(5, 0, 5, 10)]
    assert result.bbox == Rect(5, 0, 5, 10)


def test_offset_intersection():
    a = Region.from_rect(Rect(0, 0, 10, 10))
    b = Region.from_rect(Rect(5, 5, 10, 10))
    result = Region([Band(5, 10, [5, 10])])
    assert a & b == result
    assert list(result.rects()) == [Rect(5, 5, 5, 5)]
    assert result.bbox == Rect(5, 5, 5, 5)


def test_intersection_branching_1():
    a = Region([Band(0, 10, [0, 10]), Band(20, 50, [0, 10])])
    b = Region([Band(5, 25, [5, 15]), Band(35, 45, [5, 15])])
    result = Region(
        [Band(5, 10, [5, 10]), Band(20, 25, [5, 10]), Band(35, 45, [5, 10])]
    )
    assert a & b == result
    assert list(result.rects()) == [
        Rect(5, 5, 5, 5),
        Rect(5, 20, 5, 5),
        Rect(5, 35, 5, 10),
    ]
    assert result.bbox == Rect(5, 5, 5, 40)


def test_intersection_branching_2():
    a = Region([Band(0, 10, [0, 10]), Band(40, 50, [0, 10])])
    b = Region([Band(20, 30, [0, 10])])
    result = Region()
    assert a & b == result
    assert list(result.rects()) == []
    assert result.bbox is None


def test_intersection_branching_3():
    a = Region([Band(0, 10, [0, 10]), Band(15, 25, [0, 10])])
    b = Region([Band(5, 25, [5, 15])])
    result = Region([Band(5, 10, [5, 10]), Band(15, 25, [5, 10])])
    assert a & b == result
    assert list(result.rects()) == [Rect(5, 5, 5, 5), Rect(5, 15, 5, 10)]
    assert result.bbox == Rect(5, 5, 5, 20)
