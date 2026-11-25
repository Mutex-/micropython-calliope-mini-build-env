"""Raw 8-bit sample playback at 7812.5 samples per second.

Plays on pin0 by default. For the onboard speaker: ``pin_M_SLEEP.write_digital(1)``
and ``play(..., pin=pin_M_IN1)``.
"""

from typing import Iterable, Optional

from calliopemini import MicroBitDigitalPin

class AudioFrame:
    """32 samples, each 0-255 (128 is silence)."""

    def __init__(self) -> None: ...
    def __len__(self) -> int: ...
    def __getitem__(self, key: int) -> int: ...
    def __setitem__(self, key: int, value: int) -> None: ...
    def __add__(self, other: AudioFrame) -> AudioFrame: ...
    def __sub__(self, other: AudioFrame) -> AudioFrame: ...
    def __mul__(self, n: float) -> AudioFrame: ...
    def copyfrom(self, other: AudioFrame) -> None:
        """Overwrite this frame with ``other``."""

def play(
    source: Iterable[AudioFrame],
    wait: bool = True,
    pin: Optional[MicroBitDigitalPin] = None,
    return_pin: Optional[MicroBitDigitalPin] = None,
) -> None:
    """Play frames. Without ``pin`` it looks for a speaker across two of pin0-pin2, else pin0."""

def is_playing() -> bool:
    """True while frames are playing."""

def stop() -> None:
    """Stop playback."""
