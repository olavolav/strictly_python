# strictly_python

This library adds the `@strict` decorator to Python for strict typing
and fast performance, powered by [Numba](https://numba.pydata.org/).

Example:
```python
from strict_python import strict

@strict
def my_function(x: int, y: float) -> int:
    return int(y**x)
```

What this does under the hood is translates the type hints to Numba
types and triggers JIT compliation via Numba.
This means that restrictions to the arguments are the same as in Numba.

# Why is this faster?

One of the core limitations to Python performance is dynamic typing.
This means that even a seemingly trivial function like the following
is not as computationally cheap as it may seem:
```python
def add(x):
    return x + 3
```

Python needs to handle the fact that `x` can be an `int`, but it might
also be any other type that has a `__add__` function defined. In essence,
even for the most simple cases, and even with type hints, Python needs to
operate on large dictionaries (hash maps) around and do expensive memory
access, rather than simple integer addition.