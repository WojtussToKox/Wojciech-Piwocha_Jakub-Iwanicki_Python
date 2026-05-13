from typing import Callable, Generator, Any
from functools import cache

def make_generator(f):
    def generator():
        n = 1
        while True:
            yield f(n)
            n += 1
    return generator()

def make_generator_mem(f: Callable[[int], int]) -> Generator[Any, None, None]:
    return make_generator(cache(f))