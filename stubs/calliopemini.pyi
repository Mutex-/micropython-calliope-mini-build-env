"""Calliope mini v1: display, buttons, sensors, pins and buses.

The REPL starts with ``from calliopemini import *`` already done. The module is
also importable as ``microbit``, so micro:bit scripts run unchanged.
"""

from typing import Iterable, List, Literal, NoReturn, Optional, Tuple, Union, overload

import audio as audio

# The names the module has on the board. The MicroBit* classes below describe the
# objects' types (shown in error messages such as "'MicroBitDigitalPin' object has
# no attribute ..."), but they aren't attributes of the module at runtime.
__all__ = [
    "Image", "display", "button_a", "button_b", "accelerometer", "gyroscope", "compass",
    "audio", "i2c", "uart", "spi",
    "reset", "sleep", "running_time", "panic", "temperature", "scale",
    "pin0", "pin1", "pin2", "pin3", "pin4", "pin5", "pin6", "pin7", "pin8", "pin9",
    "pin10", "pin11", "pin12", "pin13", "pin14", "pin15", "pin16", "pin17", "pin19", "pin20",
    "pin_btnA", "pin_btnB", "pin_RGB", "pin_MIC", "pin_M_SLEEP", "pin_M_IN1", "pin_M_IN2",
]

_Buffer = Union[bytes, bytearray, memoryview]
_Gesture = Literal[
    "up", "down", "left", "right", "face up", "face down",
    "freefall", "3g", "6g", "8g", "shake",
]

# --- Board functions --------------------------------------------------------

def sleep(n: Union[int, float]) -> None:
    """Wait ``n`` milliseconds. The display, music and radio keep running."""

def running_time() -> int:
    """Milliseconds since the board powered on or reset."""

def temperature() -> int:
    """Temperature in degrees Celsius, read from the processor die (reads a few degrees high)."""

def scale(value: float, from_: Tuple[float, float], to: Tuple[float, float]) -> Union[int, float]:
    """Map ``value`` from the range ``from_`` to the range ``to``.

    Returns an int if both ends of ``to`` are ints, otherwise a float::

        scale(accelerometer.get_x(), from_=(-1024, 1024), to=(0, 9))
    """

def panic(n: int = 0) -> NoReturn:
    """Stop and show error code ``n`` (0-255) on the display until reset."""

def reset() -> NoReturn:
    """Restart the board. The script runs again from the top."""

# --- Image ------------------------------------------------------------------

class Image:
    """A grid of LED brightness values from 0 (off) to 9.

    ``Image('09090:99999:99999:09990:00900')``: rows separated by ``:``, one digit per LED.
    """

    @overload
    def __init__(self, string: str) -> None:
        """Build an image from rows of digits separated by ``:``."""
    @overload
    def __init__(self, width: int = 5, height: int = 5, buffer: Optional[_Buffer] = None) -> None:
        """A blank image, or one filled row by row from ``buffer`` (``width * height`` values 0-9)."""

    def width(self) -> int:
        """Width in LEDs."""
    def height(self) -> int:
        """Height in LEDs."""
    def set_pixel(self, x: int, y: int, value: int) -> None:
        """Set one pixel to 0-9. Raises TypeError on the built-in images; ``copy()`` them first."""
    def get_pixel(self, x: int, y: int) -> int:
        """Brightness 0-9 of one pixel."""
    def shift_left(self, n: int) -> Image:
        """A new image moved left by ``n`` pixels."""
    def shift_right(self, n: int) -> Image:
        """A new image moved right by ``n`` pixels."""
    def shift_up(self, n: int) -> Image:
        """A new image moved up by ``n`` pixels."""
    def shift_down(self, n: int) -> Image:
        """A new image moved down by ``n`` pixels."""
    def crop(self, x: int, y: int, w: int, h: int) -> Image:
        """A new image cut out of this one."""
    def copy(self) -> Image:
        """An editable copy."""
    def invert(self) -> Image:
        """A new image with each value replaced by ``9 - value``."""
    def fill(self, value: int) -> None:
        """Set every pixel to ``value`` (0-9), in place."""
    def blit(self, src: Image, x: int, y: int, w: int, h: int, xdest: int = 0, ydest: int = 0) -> None:
        """Copy a rectangle of ``src`` into this image, in place."""
    def __add__(self, other: Image) -> Image:
        """Add two images pixel by pixel, clipped at 9."""
    def __sub__(self, other: Image) -> Image:
        """Subtract two images pixel by pixel, clipped at 0."""
    def __mul__(self, n: float) -> Image:
        """Scale every pixel's brightness by ``n``."""
    def __truediv__(self, n: float) -> Image:
        """Divide every pixel's brightness by ``n``."""

    HEART: Image
    HEART_SMALL: Image
    HAPPY: Image
    SMILE: Image
    SAD: Image
    CONFUSED: Image
    ANGRY: Image
    ASLEEP: Image
    SURPRISED: Image
    SILLY: Image
    FABULOUS: Image
    MEH: Image
    YES: Image
    NO: Image
    CLOCK12: Image
    CLOCK1: Image
    CLOCK2: Image
    CLOCK3: Image
    CLOCK4: Image
    CLOCK5: Image
    CLOCK6: Image
    CLOCK7: Image
    CLOCK8: Image
    CLOCK9: Image
    CLOCK10: Image
    CLOCK11: Image
    ARROW_N: Image
    ARROW_NE: Image
    ARROW_E: Image
    ARROW_SE: Image
    ARROW_S: Image
    ARROW_SW: Image
    ARROW_W: Image
    ARROW_NW: Image
    TRIANGLE: Image
    TRIANGLE_LEFT: Image
    CHESSBOARD: Image
    DIAMOND: Image
    DIAMOND_SMALL: Image
    SQUARE: Image
    SQUARE_SMALL: Image
    RABBIT: Image
    COW: Image
    MUSIC_CROTCHET: Image
    MUSIC_QUAVER: Image
    MUSIC_QUAVERS: Image
    PITCHFORK: Image
    XMAS: Image
    PACMAN: Image
    TARGET: Image
    TSHIRT: Image
    ROLLERSKATE: Image
    DUCK: Image
    HOUSE: Image
    TORTOISE: Image
    BUTTERFLY: Image
    STICKFIGURE: Image
    GHOST: Image
    SWORD: Image
    GIRAFFE: Image
    SKULL: Image
    UMBRELLA: Image
    SNAKE: Image
    SCISSORS: Image
    ALL_CLOCKS: Tuple[Image, ...]
    """All 12 clock faces, for ``display.show(Image.ALL_CLOCKS, loop=True)``."""
    ALL_ARROWS: Tuple[Image, ...]
    """All 8 arrows."""

# --- Display ----------------------------------------------------------------

class MicroBitDisplay:
    """The 5x5 LED matrix. Brightness runs from 0 (off) to 9.

    Physically a 3x9 grid on pin4-pin15, so those pins aren't free while it's on.
    """

    def show(
        self,
        image: Union[Image, str, int, float, Iterable[Image], Iterable[str]],
        delay: int = 400,
        *,
        wait: bool = True,
        loop: bool = False,
        clear: bool = False,
    ) -> None:
        """Show an image, or a string, number or sequence one frame at a time, ``delay`` ms apart.

        A single character or digit is shown without scrolling.
        """
    def scroll(
        self,
        text: Union[str, int, float],
        delay: int = 150,
        *,
        wait: bool = True,
        loop: bool = False,
        monospace: bool = False,
    ) -> None:
        """Scroll ``text`` across the display; a smaller ``delay`` scrolls faster."""
    def clear(self) -> None:
        """Turn every LED off."""
    def set_pixel(self, x: int, y: int, value: int) -> None:
        """Set the LED at column ``x``, row ``y`` (0-4) to brightness 0-9."""
    def get_pixel(self, x: int, y: int) -> int:
        """Brightness 0-9 of one LED."""
    def on(self) -> None:
        """Turn the display back on and reclaim its pins."""
    def off(self) -> None:
        """Stop the display and release pin4-pin12 for other use."""
    def is_on(self) -> bool:
        """True while the display is running."""
    def read_light_level(self) -> int:
        """Ambient light 0-255, measured with the LEDs themselves."""

display: MicroBitDisplay

# --- Buttons ----------------------------------------------------------------

class MicroBitButton:
    """A button. Presses are debounced and counted in the background."""

    def is_pressed(self) -> bool:
        """True while the button is held down."""
    def was_pressed(self) -> bool:
        """True if pressed since the last call (or since boot); the call clears it."""
    def get_presses(self) -> int:
        """Number of presses since the last call; resets the count."""

button_a: MicroBitButton
"""Button A, on the left (P0.17)."""
button_b: MicroBitButton
"""Button B, on the right (P0.16)."""

# --- Sensors ----------------------------------------------------------------

class MicroBitAccelerometer:
    """The BMX055 accelerometer, about 1024 per g.

    x is negative with the button A side down, y positive with the USB edge up,
    z negative lying face up. Gestures register in a loop that keeps polling.
    """

    def get_x(self) -> int:
        """Acceleration along x."""
    def get_y(self) -> int:
        """Acceleration along y."""
    def get_z(self) -> int:
        """Acceleration along z."""
    def get_values(self) -> Tuple[int, int, int]:
        """``(x, y, z)``."""
    def get_strength(self) -> int:
        """Total acceleration (about 1024 at rest)."""
    def current_gesture(self) -> str:
        """The current gesture name, or ``''`` if none is stable yet."""
    def is_gesture(self, name: _Gesture) -> bool:
        """True if ``name`` is the current gesture."""
    def was_gesture(self, name: _Gesture) -> bool:
        """True if ``name`` happened since the last call."""
    def get_gestures(self) -> Tuple[str, ...]:
        """Gestures since the last call, oldest first; clears the history."""
    def set_range(self, g: int) -> None:
        """Measurement range in g: 2, 4, 8 or 16. Readings stay at about 1024 per g."""

accelerometer: MicroBitAccelerometer

class MicroBitGyroscope:
    """The BMX055 gyroscope: rotation rates in degrees per second, up to +-2000.

    Uses the accelerometer's axes; positive rates follow the right-hand rule. A
    flat board turned clockwise (seen from above) gives a positive z.
    """

    def get_x(self) -> int:
        """Rate around x. Lifting the USB edge gives a negative value."""
    def get_y(self) -> int:
        """Rate around y. Lifting the button B side gives a negative value."""
    def get_z(self) -> int:
        """Rate around z."""
    def get_values(self) -> Tuple[int, int, int]:
        """``(x, y, z)``, read at the same moment. Raises OSError without the sensor."""

gyroscope: MicroBitGyroscope

class MicroBitCompass:
    """The BMX055 magnetometer, in nano-tesla.

    Calibrate before relying on it: the board's own parts add an offset of
    roughly 90 uT. The calibration is lost at every reset.
    """

    def heading(self) -> int:
        """Degrees 0-359 the USB edge points to, from north. Starts calibration first if needed."""
    def calibrate(self) -> None:
        """Run the tilt-to-fill calibration: tilt until all 25 LEDs are lit."""
    def is_calibrated(self) -> bool:
        """True once calibrated (since the last reset)."""
    def clear_calibration(self) -> None:
        """Forget the calibration."""
    def get_x(self) -> int:
        """Field along x."""
    def get_y(self) -> int:
        """Field along y."""
    def get_z(self) -> int:
        """Field along z."""
    def get_field_strength(self) -> int:
        """Magnitude of the field."""

compass: MicroBitCompass

# --- Pins -------------------------------------------------------------------

class MicroBitDigitalPin:
    """A pin with digital input/output and PWM output."""

    PULL_UP: int
    PULL_DOWN: int
    NO_PULL: int

    def write_digital(self, value: int) -> None:
        """Drive the pin high (1) or low (0)."""
    def read_digital(self) -> int:
        """Read 1 or 0."""
    def write_analog(self, value: int) -> None:
        """PWM output with duty cycle 0-1023."""
    def set_analog_period(self, period: int) -> None:
        """PWM period in milliseconds (default 20 ms)."""
    def set_analog_period_microseconds(self, period: int) -> None:
        """PWM period in microseconds."""
    def get_analog_period_microseconds(self) -> int:
        """Current PWM period in microseconds."""
    def set_pull(self, value: int) -> None:
        """Internal resistor for reading: ``PULL_UP``, ``PULL_DOWN`` or ``NO_PULL``."""
    def get_pull(self) -> int:
        """The current pull setting."""
    def get_mode(self) -> str:
        """What the pin is used for, e.g. ``'unused'``, ``'display'``, ``'music'``, ``'i2c'``."""

class MicroBitAnalogDigitalPin(MicroBitDigitalPin):
    """A pin that can also read voltages."""

    def read_analog(self) -> int:
        """Voltage as 0-1023 (0 V to 3.3 V)."""

class MicroBitTouchPin(MicroBitAnalogDigitalPin):
    """A pin that can also detect touch."""

    def is_touched(self) -> bool:
        """True while a finger bridges the pin and GND."""

pin0: MicroBitDigitalPin
"""Pad P0 (P0.0). Default output for audio and speech. Not a touch pin."""
pin1: MicroBitTouchPin
"""Pad P1 (P0.1)."""
pin2: MicroBitTouchPin
"""Pad P2 (P0.2)."""
pin3: MicroBitAnalogDigitalPin
"""P0.3, the same GPIO as the microphone (pin_MIC)."""
pin4: MicroBitAnalogDigitalPin
"""LED column 1 (P0.4). Free after ``display.off()``."""
pin5: MicroBitAnalogDigitalPin
"""LED column 2 (P0.5). Free after ``display.off()``."""
pin6: MicroBitAnalogDigitalPin
"""LED column 3 (P0.6). Free after ``display.off()``."""
pin7: MicroBitDigitalPin
"""LED column 4 (P0.7). Free after ``display.off()``."""
pin8: MicroBitDigitalPin
"""LED column 5 (P0.8). Not guarded: using it while the display is on fights the matrix."""
pin9: MicroBitDigitalPin
"""LED column 6 (P0.9). Free after ``display.off()``."""
pin10: MicroBitDigitalPin
"""LED column 7 (P0.10). Free after ``display.off()``."""
pin11: MicroBitDigitalPin
"""LED column 8 (P0.11). Free after ``display.off()``."""
pin12: MicroBitDigitalPin
"""LED column 9 (P0.12). Not guarded."""
pin13: MicroBitDigitalPin
"""LED row 1 (P0.13); default SPI SCK."""
pin14: MicroBitDigitalPin
"""LED row 2 (P0.14); default SPI MISO."""
pin15: MicroBitDigitalPin
"""LED row 3 (P0.15); default SPI MOSI."""
pin16: MicroBitAnalogDigitalPin
"""P0.26, labelled RX."""
pin17: MicroBitAnalogDigitalPin
"""P0.27, labelled TX."""
pin19: MicroBitDigitalPin
"""I2C SCL (P0.19), shared with the BMX055. Reserved for i2c."""
pin20: MicroBitDigitalPin
"""I2C SDA (P0.20), shared with the BMX055. Reserved for i2c."""
pin_btnA: MicroBitDigitalPin
"""Button A (P0.17). ``read_digital()`` works; prefer ``button_a``."""
pin_btnB: MicroBitDigitalPin
"""Button B (P0.16). ``read_digital()`` works; prefer ``button_b``."""
pin_RGB: MicroBitDigitalPin
"""The RGB LED (P0.18), a WS2812: ``neopixel.NeoPixel(pin_RGB, 1)``."""
pin_MIC: MicroBitAnalogDigitalPin
"""The microphone (P0.3): ``read_analog()`` gives the level."""
pin_M_SLEEP: MicroBitDigitalPin
"""Motor driver enable (P0.28). Held by music while it plays."""
pin_M_IN1: MicroBitDigitalPin
"""Motor driver input 1 (P0.29), drives the speaker. Default music output."""
pin_M_IN2: MicroBitDigitalPin
"""Motor driver input 2 (P0.30). Held low by music while it plays."""

# --- Buses ------------------------------------------------------------------

class MicroBitI2C:
    """I2C controller with 7-bit addresses. Defaults to pin20 (SDA) / pin19 (SCL)."""

    def init(
        self,
        freq: int = 100000,
        sda: Optional[MicroBitDigitalPin] = None,
        scl: Optional[MicroBitDigitalPin] = None,
    ) -> None:
        """Configure the bus. Without pins it uses pin20/pin19, shared with the onboard BMX055."""
    def scan(self) -> List[int]:
        """Addresses that answered. The BMX055 shows as 0x10, 0x18 and 0x68."""
    def read(self, addr: int, n: int, repeat: bool = False) -> bytes:
        """Read ``n`` bytes. ``repeat=True`` skips the stop condition."""
    def write(self, addr: int, buf: _Buffer, repeat: bool = False) -> None:
        """Write a buffer. ``repeat=True`` skips the stop condition."""

i2c: MicroBitI2C

class MicroBitUART:
    """Serial port; by default the USB serial the REPL uses."""

    ODD: int
    EVEN: int

    def init(
        self,
        baudrate: int = 9600,
        bits: int = 8,
        parity: Optional[int] = None,
        stop: int = 1,
        *,
        pins: Optional[Tuple[MicroBitDigitalPin, MicroBitDigitalPin]] = None,
        tx: Optional[MicroBitDigitalPin] = None,
        rx: Optional[MicroBitDigitalPin] = None,
    ) -> None:
        """Reconfigure the port. This takes it away from the REPL until reset."""
    def any(self) -> bool:
        """True if received bytes are waiting."""
    def read(self, nbytes: Optional[int] = None) -> Optional[bytes]:
        """Read what's available (up to ``nbytes``); None on timeout."""
    def readline(self) -> Optional[bytes]:
        """Read up to and including a newline; None on timeout."""
    def readinto(self, buf: bytearray, nbytes: Optional[int] = None) -> Optional[int]:
        """Read into ``buf``; returns the number of bytes, or None on timeout."""
    def write(self, buf: Union[str, _Buffer]) -> Optional[int]:
        """Send a string or bytes; returns the number of bytes written."""

uart: MicroBitUART

class MicroBitSPI:
    """SPI controller. The default pins (pin13-pin15) are the LED matrix rows."""

    def init(
        self,
        baudrate: int = 1000000,
        bits: int = 8,
        mode: int = 0,
        *,
        sclk: Optional[MicroBitDigitalPin] = None,
        mosi: Optional[MicroBitDigitalPin] = None,
        miso: Optional[MicroBitDigitalPin] = None,
    ) -> None:
        """Configure the bus; ``mode`` 0-3 sets clock polarity and phase."""
    def write(self, buf: _Buffer) -> None:
        """Send bytes."""
    def read(self, nbytes: int, sendbyte: int = 0) -> bytes:
        """Read ``nbytes`` while sending ``sendbyte``."""
    def write_readinto(self, out: _Buffer, in_: bytearray, /) -> None:
        """Send ``out`` and fill ``in_`` at the same time; both the same length."""

spi: MicroBitSPI
