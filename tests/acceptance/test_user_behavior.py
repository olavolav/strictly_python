from strict_python import strict

def test_basic_function():
    @strict
    def my_function(x: int, y: float) -> int:
        return int(y**x)

    my_function(2, 3.14)