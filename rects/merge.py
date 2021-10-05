def merge(a, b):
    """
    Emit in/out signals whenever a threshold is cross.
    """
    a = iter(a)
    b = iter(b)

    current_a = next(a, None)
    current_b = next(b, None)

    in_a = 0
    in_b = 0

    while current_a is not None and current_b is not None:
        old_a, old_b = current_a, current_b

        if old_a >= old_b:
            in_b ^= 1
            current_b = next(b, None)

        if old_b >= old_a:
            in_a ^= 1
            current_a = next(a, None)

        yield in_a, in_b
