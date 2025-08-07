import inspect
from typing import get_type_hints, Callable
from numba import njit, types

PYTHON_TO_NUMBA = {
    int: types.int64,
    float: types.float64,
    bool: types.boolean,
    str: types.unicode_type,
    None: types.void,
}

def python_type_to_numba(py_type):
    try:
        return PYTHON_TO_NUMBA[py_type]
    except KeyError:
        raise TypeError(f"No Numba equivalent for type: {py_type}")

def strict(func: Callable):
    sig = inspect.signature(func)
    hints = get_type_hints(func)

    arg_types = []
    for param in sig.parameters.values():
        if param.name not in hints:
            raise TypeError(f"Missing type annotation for argument: {param.name}")
        arg_types.append(python_type_to_numba(hints[param.name]))

    if 'return' not in hints:
        raise TypeError("Missing return type annotation")
    return_type = python_type_to_numba(hints['return'])

    numba_sig = return_type(*arg_types)
    compiled_func = njit(numba_sig)(func)  # ✅ no need for nopython=True
    return compiled_func