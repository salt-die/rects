def merge(a, b):
    """
    Emit in/out signals whenever a threshold is crossed.
    """
    a = iter(a)
    b = iter(b)

    current_a = next(a, None)
    current_b = next(b, None)

    in_a = 0
    in_b = 0

    while current_a is not None and current_b is not None:
        threshold = min(current_a, current_b)

        if current_a == threshold:
            in_a ^= 1
            current_a = next(a, None)

        if current_b == threshold:
            in_b ^= 1
            current_b = next(b, None)

        yield in_a, in_b, threshold

    if current_a is not None:
        in_a ^= 1
        yield in_a, in_b, current_a

        for current_a in a:
            in_a ^= 1
            yield in_a, in_b, current_a

    elif current_b is not None:
        in_b ^= 1
        yield in_a, in_b, current_b

        for current_b in b:
            in_b ^= 1
            yield in_a, in_b, current_b
