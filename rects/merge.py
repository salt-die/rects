from typing import NamedTuple


class ScanState(NamedTuple):
    wall: int
    in_a: bool
    in_b: bool


class Walls:
    __slots__ = 'iterable', 'inside', 'wall'

    def __init__(self, iterable):
        self.iterable = iter(iterable)

        self.inside = True  # Sets to false on first __next__ call.
        self.wall = None

        next(self)

    def __bool__(self):
        return self.wall is not None

    def __lt__(self, other):
        return self.wall < other.wall

    def __next__(self):
        try:
            return self.wall
        finally:
            self.inside ^= True
            self.wall = next(self.iterable, None)


def merge(a, b):
    """
    Emit in/out signals whenever a threshold is crossed.
    """
    a = Walls(a)
    b = Walls(b)

    while a and b:
        wall = min(a, b).wall

        if a.wall == wall:
            next(a)

        if b.wall == wall:
            next(b)

        yield ScanState(wall, a.inside, b.inside)

    c = a or b
    while c:
        yield ScanState(next(c), a.inside, b.inside)
