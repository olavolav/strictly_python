import pytest
import numpy as np
from numpy.typing import NDArray

from strictly_python import strict


def test_basic_function():
    @strict
    def my_function(x: int, y: float) -> int:
        return int(y**x)

    result = my_function(2, 3.14)
    assert abs(result - int(3.14 * 3.14)) < 1e-4


def test_strict_with_missing_type_hints_should_fail():
    with pytest.raises(TypeError):

        @strict
        def my_function(x: int, y) -> int:
            return int(y**x)


def test_strict_with_object_type_hints_should_fail():
    with pytest.raises(TypeError):

        @strict
        def my_function(x: int, y: dict) -> int:
            return int(y**x)

        my_function(3, {"apple": "tasty"})


def test_strict_with_array_as_argument():
    @strict
    def my_function(x: NDArray) -> int:
        return x[0] + x[-1]

    array = np.array([1, 2, 3, 4, 5])
    result = my_function(array)
    assert result == 6
