import os
import inspect
from typing import get_type_hints


def _identity_decorator(f):
    """
    No-op decorator used as a fallback when JIT compilation is disabled or unsupported.
    This simply returns the function unchanged.
    """
    return f


def make_strict():
    """
    Factory that creates the @strict decorator.
    This lets us decide at import time whether to return a Numba-based implementation
    or a no-op fallback, depending on the environment.
    """
    # Allow users to disable JIT compilation entirely via environment variable.
    # This is useful for unsupported platforms or debugging.
    if os.environ.get("STRICT_DISABLE", "").lower() in {"1", "true", "yes", "on"}:
        return _identity_decorator

    try:
        # Try importing Numba's njit for compilation.
        from numba import njit
    except Exception:
        # If Numba is missing or cannot be imported (unsupported platform),
        # fall back to the no-op decorator so code still runs.
        return _identity_decorator

    def strict(func=None, *, cache=True, fastmath=False, parallel=False):
        """
        @strict decorator:
        - Ensures every function parameter and the return type has an annotation.
        - Compiles the function with numba.njit to machine code (nopython mode by default).
        - Returns the Numba Dispatcher object directly, so calls from one @strict
          function to another stay entirely in native code without Python overhead.
        - If Numba is unavailable or disabled, falls back to leaving the function as-is.

        Parameters:
            func: The function being decorated (or None if using keyword arguments).
            cache (bool): Whether to cache compiled machine code across runs.
            fastmath (bool): Allow unsafe floating-point optimizations.
            parallel (bool): Enable parallel execution (Numba's prange, etc.).
        """

        def deco(f):
            # Require presence of annotations for all parameters and the return type.
            # This enforces a discipline: functions must be fully type-annotated.
            sig = inspect.signature(f)
            hints = get_type_hints(f)  # resolves forward references, if any

            for name in sig.parameters:
                if name not in hints:
                    raise TypeError(
                        f"Missing type hint for parameter '{name}' in '{f.__name__}'"
                    )
            if "return" not in hints:
                raise TypeError(f"Missing return type hint in '{f.__name__}'")

            # Compile with Numba's njit. This will run type inference on first call
            # and fail at runtime if the argument types are unsupported.
            dispatcher = njit(cache=cache, fastmath=fastmath, parallel=parallel)(f)

            # For convenience, expose the original Python function as an attribute.
            # This is *not* used in compiled paths; calling it from jitted code
            # would reintroduce Python overhead.
            dispatcher.python = f

            # Return the compiled Dispatcher directly so it can be called from other
            # jitted functions without a Python round-trip.
            return dispatcher

        # Support both @strict and @strict(...)
        return deco(func) if func is not None else deco

    return strict


# Public decorator: this is what users will import and apply to their functions.
strict = make_strict()
