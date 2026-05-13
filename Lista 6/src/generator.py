from typing import Callable, Generator, Any
from functools import cache
from itertools import islice

def make_generator(f):
    def generator():
        n = 1
        while True:
            yield f(n)
            n += 1
    return generator()

def make_generator_mem(f: Callable[[int], int]) -> Generator[Any, None, None]:
    return make_generator(cache(f))


def main():
    @cache
    def fib(n):
        return n if n <= 1 else fib(n - 1) + fib(n - 2)

    print("Fibonacci (pierwsze 10):")
    print(list(islice(make_generator(fib), 10)))

    from math import factorial
    catalan = lambda n: factorial(2 * n) // (factorial(n + 1) * factorial(n))

    print("\nLiczby Catalana (pierwsze 10):")
    print(list(islice(make_generator(catalan), 10)))



    print("\n--- make_generator_mem ---")
    def fib_rec(n):
        return n if n <= 1 else fib_rec(n - 1) + fib_rec(n - 2)

    print("\nFibonacci z make_generator_mem (pierwsze 10):")
    print(list(islice(make_generator_mem(fib_rec), 10)))

if __name__ == "__main__":
    main()