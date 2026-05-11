def forall(pred, iterable) -> bool:
    return all(map(pred, iterable))

def exists(pred, iterable) -> bool:
    return any(map(pred, iterable))

def atleast(n, pred, iterable) -> bool:
    return sum(map(pred, iterable)) >= n

def atmost(n, pred, iterable) -> bool:
    return sum(map(pred, iterable)) <= n
