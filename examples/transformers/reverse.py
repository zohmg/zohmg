def compare_tuples(p,q):
    """
    Compare tuples by their first element.
    """
    x,y = p
    u,v = q
    if x < u: return 1
    if x > u: return -1
    return 0


def transform(payload):
    """
    Simple transformer which reverses input.
    """
    data = sorted(payload,compare_tuples)
    return data
