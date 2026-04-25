def forall(pred, iterable) -> bool:
    return all(map(pred, iterable))

def any(pred, iterable) -> bool:
    return any(map(pred, iterable))

def atleast(n, pred, iterable) -> bool:
    return sum(map(pred, iterable)) >= n

def atmsost(n, pred, iterable) -> bool:
    return sum(map(pred, iterable)) <= n
