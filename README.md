# rects

A library for unions, intersections, subtractions, and xors of rectangles (for managing windows).

Regions
-------
Say one has a list of windows that may or may not overlap, and one wants to draw them efficiently.
Ideally, we don't draw parts of windows that are covered by other windows:

```
    +------------+
    |            |
    |        +-----------+
    |        |     a     |
    |        +-----------+
    |            |
    +------------+
```

After `a` is drawn, we need to represent the area `b`:
```
    +------------+
    |            |
    |        +---+
    |   b    |
    |        +---+
    |            |
    +------------+
```

This is done by dividing the area into a series of mutually exclusive horizontal bands:
```
    +------------+
    |   band 1   |
    |--------+---+
    | band 2 |
    |--------+---+
    |   band 3   |
    +------------+
```

Each band is a vertical interval and a list of walls. Each contiguous pair of walls indicates a new rect in the band.
A `Region` is a list of sorted, mutually exclusive bands.

Using `rects`
------------
To use rects, just construct an initial `Region`, `r`, from some rect and iteratively
`union`, `intersect`, `subtract`, or `xor` `r` with other rects:
```py
In [1]: from rects import *
   ...: r = Region(Rect(Interval(0, 100), Interval(0, 200)))

In [2]: r
Out[2]: Region(bands=[Band(topbottom=Interval(start=0, stop=100), walls=[0, 200])])

In [3]: s = Rect(Interval(10, 50), Interval(25, 100)); t = Rect(Interval(45, 95), Interval(75, 200))

In [4]: r - s - t
Out[4]: Region(bands=[
            Band(topbottom=Interval(start=0, stop=10), walls=[0, 200]),
            Band(topbottom=Interval(start=10, stop=45), walls=[0, 25, 100, 200]),
            Band(topbottom=Interval(start=45, stop=50), walls=[0, 25]),
            Band(topbottom=Interval(start=50, stop=95), walls=[0, 75]),
            Band(topbottom=Interval(start=95, stop=100), walls=[0, 200]),
            ]
        )
```