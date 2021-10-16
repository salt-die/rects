from math import inf

def merge(a, b, operation):
    """
    Merge two lists of (sorted endpoints of) intervals given a
    set operation (union, intersection, subtraction, xor).
    """
    inside_a = False
    inside_b = False
    inside_region = False

    a = iter(a)
    b = iter(b)

    current_a = next(a, inf)
    current_b = next(b, inf)
    threshold = min(current_a, current_b)

    walls = [ ]

    while threshold != inf:
        if current_a == threshold:
            inside_a ^= True
            current_a = next(a, inf)

        if current_b == threshold:
            inside_b ^= True
            current_b = next(b, inf)

        if operation(inside_a, inside_b) != inside_region:
            inside_region ^= True
            walls.append(threshold)

        threshold = min(current_a, current_b)

    return walls
