"""Low-level access to the nRF51822."""

from typing import NoReturn

from calliopemini import MicroBitDigitalPin

class _Mem:
    def __getitem__(self, address: int) -> int: ...
    def __setitem__(self, address: int, value: int) -> None: ...

mem8: _Mem
"""Read or write a byte of memory: ``mem8[address]``."""
mem16: _Mem
"""Read or write 16 bits of memory."""
mem32: _Mem
"""Read or write 32 bits of memory or a register."""

def unique_id() -> bytes:
    """8 bytes unique to this chip."""

def reset() -> NoReturn:
    """Restart the board."""

def freq() -> int:
    """CPU frequency in Hz (16 MHz)."""

def disable_irq() -> int:
    """Pause interrupts; pass the result to ``enable_irq``."""

def enable_irq(state: int) -> None:
    """Restore interrupts from the value ``disable_irq`` returned."""

def time_pulse_us(pin: MicroBitDigitalPin, pulse_level: int, timeout_us: int = 1000000) -> int:
    """Length of the next pulse at ``pulse_level`` in microseconds; negative on timeout."""
