# rects

A library for unions, intersections, subtractions, and xors of rectangles (for managing windows).

Regions
-------
Given a list of overlapping windows, how can they be efficiently rendered?
Ideally, areas of windows covered by other windows are never drawn:

```
    +------------+   +--------+
    |            |   |        |
    |        +-----------+    |
    |        |     a     |    |
    |        +-----------+----+
    |            |
    +------------+
```

But how to represent the above area after subtracting `a`?
```
    +------------+   +--------+
    |            |   |    c   |
    |        +---+   +---+    |
    |   b    |           |    |
    |        +---+       +----+
    |            |
    +------------+
```

One method is to divide the area into a series of mutually exclusive horizontal bands:
```
    +------------+   +--------+
    |            |   |        |
    +--------+---+   +---+----+
    | a      | b         | c  | d   <- 2nd band with walls at a, b, c, d.
    +--------+---+       +----+
    |            |
    +------------+
```

Each band is a vertical interval and a list of walls. Each contiguous pair of walls indicates a new rect in the band.
A `Region` is a list of sorted, mutually exclusive bands.

Using `rects`
------------
To use rects, construct an initial `Region`, `r`, from some rect and iteratively
`+`, `-`, `&`, or `^` with other regions:
```py
>>> from rects import *
>>> r = Region.from_rect(Rect(0, 0, 100, 200))
>>> r
Region(bands=[Band(y1=0, y2=100, walls=[0, 200])])
>>> s = Region.from_rect(Rect(10, 25, 40, 75))
>>> t = Region.from_rect(Rect(45, 75, 50, 125))
>>> r - s - t
Region(bands=[
    Band(y1=0, y2=10, walls=[0, 200]),
    Band(y1=10, y2=45, walls=[0, 25, 100, 200]),
    Band(y1=45, y2=50, walls=[0, 25]),
    Band(y1=50, y2=95, walls=[0, 75]),
    Band(y1=95, y2=100, walls=[0, 200])
])
>>> list(_.rects())
[
    Rect(y=0, x=0, height=10, width=200),
    Rect(y=10, x=0, height=35, width=25),
    Rect(y=10, x=100, height=35, width=100),
    Rect(y=45, x=0, height=5, width=25),
    Rect(y=50, x=0, height=45, width=75),
    Rect(y=95, x=0, height=5, width=200)
]
```