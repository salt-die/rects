from typing import NamedTuple


class ScanState(NamedTuple):
    threshold: int
    in_a: bool
    in_b: bool

def merge(a, b):
    """
    Emit in/out signals whenever a threshold is crossed.
    """
    a = iter(a)
    b = iter(b)

    current_a = next(a, None)
    current_b = next(b, None)

    inside_a = False
    inside_b = False

    while current_a is not None and current_b is not None:
        threshold = min(current_a, current_b)

        if current_a == threshold:
            current_a = next(a, None)
            inside_a ^= True

        if current_b == threshold:
            current_b = next(b, None)
            inside_b ^= True

        yield ScanState(threshold, inside_a, inside_b)

    if current_a is not None:
        while current_a:
            inside_a ^= True
            yield ScanState(current_a, inside_a, inside_b)
            current_a = next(a, None)

    elif current_b is not None:
        while current_b:
            inside_b ^= True
            yield ScanState(current_b, inside_a, inside_b)
            current_b = next(a, None)
