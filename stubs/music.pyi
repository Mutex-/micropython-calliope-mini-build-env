"""Notes and melodies as square waves, on the onboard speaker by default.

Notes are written ``NOTE[octave][:duration]``, e.g. ``'c4:4'``, ``'r:2'`` for a
rest. Octave and duration carry over to the next note.
"""

from typing import Optional, Sequence, Tuple, Union

from calliopemini import MicroBitDigitalPin

_Music = Union[str, Sequence[str]]

def play(
    music: _Music,
    pin: Optional[MicroBitDigitalPin] = ...,
    wait: bool = True,
    loop: bool = False,
) -> None:
    """Play a note, a list of notes or a built-in tune.

    ``pin`` defaults to the onboard speaker (``pin_M_IN1``; the motor driver is
    woken only while sound plays). Pass ``pin=pin0`` for pad P0.
    """

def pitch(
    frequency: int,
    duration: int = -1,
    pin: Optional[MicroBitDigitalPin] = ...,
    wait: bool = True,
) -> None:
    """Play ``frequency`` Hz. ``duration=-1`` plays until ``stop()``."""

def stop(pin: Optional[MicroBitDigitalPin] = ...) -> None:
    """Stop playback (on the speaker by default)."""

def set_tempo(*, ticks: int = 4, bpm: int = 120) -> None:
    """Set ticks per beat and beats per minute."""

def get_tempo() -> Tuple[int, int]:
    """``(bpm, ticks)``."""

def reset() -> None:
    """Back to 4 ticks per beat, 120 bpm, octave 4, duration 4."""

DADADADUM: Tuple[str, ...]
ENTERTAINER: Tuple[str, ...]
PRELUDE: Tuple[str, ...]
ODE: Tuple[str, ...]
NYAN: Tuple[str, ...]
RINGTONE: Tuple[str, ...]
FUNK: Tuple[str, ...]
BLUES: Tuple[str, ...]
BIRTHDAY: Tuple[str, ...]
WEDDING: Tuple[str, ...]
FUNERAL: Tuple[str, ...]
PUNCHLINE: Tuple[str, ...]
PYTHON: Tuple[str, ...]
BADDY: Tuple[str, ...]
CHASE: Tuple[str, ...]
BA_DING: Tuple[str, ...]
WAWAWAWAA: Tuple[str, ...]
JUMP_UP: Tuple[str, ...]
JUMP_DOWN: Tuple[str, ...]
POWER_UP: Tuple[str, ...]
POWER_DOWN: Tuple[str, ...]
