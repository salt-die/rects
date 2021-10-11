from typing import NamedTuple


class ScanState(NamedTuple):
    wall: int
    in_a: bool
    in_b: bool


class Walls:
    __slots__ = 'iterable', 'inside', 'wall'

    def __init__(self, iterable):
        self.iterable = iter(iterable)

        self.inside = True
        self.wall = None

        self.next_wall()

    def __bool__(self):
        return self.wall is not None

    def __lt__(self, other):
        return self.wall < other.wall

    def next_wall(self):
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
            a.next_wall()

        if b.wall == wall:
            b.next_wall()

        yield ScanState(wall, a.inside, b.inside)

    c = a or b
    while c:
        wall = c.wall
        c.next_wall()
        yield ScanState(wall, a.inside, b.inside)
