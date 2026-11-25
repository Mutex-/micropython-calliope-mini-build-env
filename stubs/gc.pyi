"""Garbage collector. With about 9 KB of heap, ``collect()`` before big allocations helps."""

from typing import Optional

def collect() -> None:
    """Run a collection now."""

def enable() -> None:
    """Enable automatic collection."""

def disable() -> None:
    """Disable automatic collection."""

def isenabled() -> bool:
    """True if automatic collection is enabled."""

def mem_alloc() -> int:
    """Bytes of heap in use."""

def mem_free() -> int:
    """Bytes of heap free."""

def threshold(amount: int = ...) -> Optional[int]:
    """Get or set the allocation amount that triggers a collection."""
