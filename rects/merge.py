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

    while current_a is not None and current_b is not None:
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

    while current_a is not None:
        inside_a ^= True

        if operation(inside_a, inside_b) != inside_region:
            inside_region ^= True
            walls.append(current_a)

        current_a = next(a, None)

    while current_b is not None:
        inside_b ^= True

        if operation(inside_a, inside_b) != inside_region:
            inside_region ^= True
            walls.append(current_b)

        current_b = next(b, None)

    return walls
