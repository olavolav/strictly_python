# strict_python

This library adds the `@strict` decorator to Python for strict typing
and fast performance, powered by Numba.

Example:
```python3
from strict_python import strict

@strict
def my_function(x: int, y: float) -> int:
    return int(y**x)
```