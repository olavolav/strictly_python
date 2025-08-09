import inspect
from typing import get_type_hints
from numba import njit
from numba.core.errors import TypingError, LoweringError


def strict(func=None, *, cache=True, fastmath=False, parallel=False):
    """
    Strict = compile-or-fail with friendly errors:
      - Enforces presence of type hints for all params + return at decoration time
      - Uses Numba inference in nopython mode on first call (via njit)
      - On failure, raises TypeError with a short summary first, then full Numba details
    """

    def deco(f):
        # Require annotations for all params + return
        sig = inspect.signature(f)
        hints = get_type_hints(f)
        for name in sig.parameters:
            if name not in hints:
                raise TypeError(f"Missing type hint for '{name}' in '{f.__name__}'")
        if "return" not in hints:
            raise TypeError(f"Missing return type hint in '{f.__name__}'")

        compiled = njit(cache=cache, fastmath=fastmath, parallel=parallel)(f)

        def wrapper(*args, **kwargs):
            try:
                return compiled(*args, **kwargs)
            except (TypingError, LoweringError) as e:
                # Short, Pythonic summary first
                short = getattr(e, "msg", None) or str(e).splitlines()[0]
                long = str(e).rstrip()
                msg = f"Strict typing failed: {short}\n\n--- Numba details ---\n{long}"
                # Suppress chained Numba traceback; we included details in the message
                raise TypeError(msg) from None

        return wrapper

    return deco(func) if func is not None else deco
