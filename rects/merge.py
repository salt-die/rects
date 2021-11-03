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

    current_a = next(a, None)
    current_b = next(b, None)

    walls = [ ]

    while current_a is not None or current_b is not None:
        match (current_a, current_b):
            case (None, _):
                threshold = current_b
            case (_, None):
                threshold = current_a
            case _:
                threshold = min(current_a, current_b)

        if current_a == threshold:
            inside_a ^= True
            current_a = next(a, None)

        if current_b == threshold:
            inside_b ^= True
            current_b = next(b, None)

        if operation(inside_a, inside_b) != inside_region:
            inside_region ^= True
            walls.append(threshold)

    return walls
