"""MicroPython internals."""

from typing import Callable, Optional, TypeVar

_T = TypeVar("_T")
_F = TypeVar("_F", bound=Callable[..., object])

def asm_thumb(func: _F) -> _F:
    """Compile the function body as inline ARM Thumb assembler (``mov(r0, 1)``, ``label(L)`` ...).

    A compiler directive rather than a runtime attribute: it works as a
    decorator but ``hasattr(micropython, 'asm_thumb')`` is False. Type checkers
    can't follow the assembler body.
    """

def const(expr: _T) -> _T:
    """Declare a constant; saves RAM for module-level ``NAME = const(1)``."""

def mem_info(verbose: int = ...) -> None:
    """Print memory usage."""

def qstr_info(verbose: int = ...) -> None:
    """Print interned-string usage."""

def stack_use() -> int:
    """Bytes of stack in use."""

def heap_lock() -> None:
    """Make heap allocations raise MemoryError."""

def heap_unlock() -> None:
    """Allow heap allocations again."""

def kbd_intr(chr: int) -> None:
    """Character that raises KeyboardInterrupt (-1 disables Ctrl-C)."""

def opt_level(level: int = ...) -> Optional[int]:
    """Get or set the compiler optimisation level."""
