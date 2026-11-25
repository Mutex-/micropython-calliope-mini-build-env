"""Timing. Also importable as ``time``."""

from typing import Union

def sleep(seconds: Union[int, float]) -> None:
    """Wait in seconds (floats allowed)."""

def sleep_ms(ms: int) -> None:
    """Wait in milliseconds."""

def sleep_us(us: int) -> None:
    """Wait in microseconds."""

def ticks_ms() -> int:
    """A millisecond counter that wraps around; compare values with ``ticks_diff``."""

def ticks_us() -> int:
    """A microsecond counter that wraps around; compare values with ``ticks_diff``."""

def ticks_add(ticks: int, delta: int) -> int:
    """Wrap-safe ``ticks + delta``."""

def ticks_diff(ticks1: int, ticks2: int) -> int:
    """Wrap-safe ``ticks1 - ticks2``."""
