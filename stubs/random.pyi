"""Hardware-seeded random numbers (MicroPython subset of ``random``)."""

from typing import Sequence, TypeVar, overload

_T = TypeVar("_T")

def getrandbits(n: int) -> int:
    """An integer with ``n`` random bits (n <= 30)."""

def seed(n: int) -> None:
    """Fixed seed for repeatable sequences."""

def randint(a: int, b: int) -> int:
    """An integer with ``a <= n <= b``."""

@overload
def randrange(stop: int) -> int: ...
@overload
def randrange(start: int, stop: int, step: int = 1) -> int:
    """An integer from ``range(start, stop, step)``."""

def choice(seq: Sequence[_T]) -> _T:
    """One random element of a non-empty sequence."""

def random() -> float:
    """A float in [0.0, 1.0)."""

def uniform(a: float, b: float) -> float:
    """A float between ``a`` and ``b``."""
