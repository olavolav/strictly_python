import pytest

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
