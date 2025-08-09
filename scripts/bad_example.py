"""
A simple illustration of the cost of Python's flexibility.

`x + 3` can literally mean anything. We should not do that of course for reasons of
readability and simplicity, but it means that it is much harder for the compiler to
identify optimizations.
"""


class BadIdea:
    def __init__(self, i: str):
        self.i = i

    def __add__(self, y):
        if isinstance(y, int):
            return BadIdea(self.i + ("sugar" * y))
        else:
            raise "not implemented"

    def __str__(self) -> str:
        return f"BadIdea(i = {self.i})"


instance = BadIdea("honey")
print(instance)
print(instance + 3)
