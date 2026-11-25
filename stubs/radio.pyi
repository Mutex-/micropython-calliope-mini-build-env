"""Simple packet radio, compatible with micro:bit MicroPython radio on the same settings.

It's off until ``on()``. Devices hear each other with the same channel,
address, group and data rate.
"""

from typing import Optional, Tuple

RATE_250KBIT: int
RATE_1MBIT: int
RATE_2MBIT: int

def on() -> None:
    """Start the radio."""

def off() -> None:
    """Stop the radio (saves power)."""

def reset() -> None:
    """Restore the default settings."""

def config(
    *,
    length: int = 32,
    queue: int = 3,
    channel: int = 7,
    power: int = 6,
    address: int = 0x75626974,
    group: int = 0,
    data_rate: int = ...,
) -> None:
    """Change any of the settings: ``channel`` 0-83, ``power`` 0-7, ``length`` up to 251 bytes."""

def send(message: str) -> None:
    """Send a string."""

def receive() -> Optional[str]:
    """The next string, or None if the queue is empty."""

def send_bytes(message: bytes) -> None:
    """Send bytes."""

def receive_bytes() -> Optional[bytes]:
    """The next message as bytes, or None."""

def receive_bytes_into(buffer: bytearray) -> Optional[int]:
    """Copy the next message into ``buffer``; its length, or None."""

def receive_full() -> Optional[Tuple[bytes, int, int]]:
    """``(message, rssi, timestamp_us)`` for the next message, or None."""
