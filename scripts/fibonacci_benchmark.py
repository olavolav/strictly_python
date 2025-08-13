"""
Testing performance of computing Fibonacci numbers in pure Python and using `@strict`.

Note that this is a slightly artificial test since it ignores caching strategies.
"""

import time

from strictly_python import strict


# Pure Python Fibonacci
def fib_py(n: int) -> int:
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


# JIT-compiled Fibonacci
@strict
def fib_strict(n: int) -> int:
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def bench(fn, arg, warmup=1, repeats=5):
    # Warmup to exclude JIT compile time for strict
    for _ in range(warmup):
        fn(arg)
    times = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        fn(arg)
        t1 = time.perf_counter()
        times.append(t1 - t0)
    return sum(times) / len(times)


if __name__ == "__main__":
    N = 100_000  # Large enough to measure differences

    # Correctness check
    assert fib_py(10) == fib_strict(10)

    t_py = bench(fib_py, N)
    t_strict = bench(fib_strict, N)

    print(f"fib_py     : {t_py * 1000:.2f} ms")
    print(f"fib_strict : {t_strict * 1000:.2f} ms")
    if t_strict > 0:
        print(f"Speedup: {t_py / t_strict:.1f}×")
