"""WS2812 LED strips, including the onboard RGB LED: ``NeoPixel(pin_RGB, 1)``."""

from typing import Tuple

from calliopemini import MicroBitDigitalPin

class NeoPixel:
    def __init__(self, pin: MicroBitDigitalPin, n: int, bpp: int = 3) -> None:
        """A strip of ``n`` LEDs on ``pin``; ``bpp=4`` for RGBW strips."""
    def __getitem__(self, key: int) -> Tuple[int, ...]:
        """The colour of one LED."""
    def __setitem__(self, key: int, value: Tuple[int, ...]) -> None:
        """Set one LED, e.g. ``np[0] = (0, 40, 30)``; values 0-255 in (r, g, b) order."""
    def __len__(self) -> int: ...
    def clear(self) -> None:
        """Switch all LEDs off."""
    def show(self) -> None:
        """Send the colours to the strip."""
