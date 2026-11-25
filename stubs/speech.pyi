"""A small English speech synthesizer (SAM). Output goes through ``audio`` (pin0); it uses a lot of RAM."""

def say(words: str, *, pitch: int = 64, speed: int = 72, mouth: int = 128, throat: int = 128, debug: bool = False) -> None:
    """Speak English text. Values run 0-255; a lower ``speed`` talks faster."""

def pronounce(phonemes: str, *, pitch: int = 64, speed: int = 72, mouth: int = 128, throat: int = 128, debug: bool = False) -> None:
    """Speak a phoneme string directly."""

def sing(phonemes: str, *, pitch: int = 64, speed: int = 72, mouth: int = 128, throat: int = 128, debug: bool = False) -> None:
    """Like ``pronounce``, with ``#NN`` pitch markers before phonemes."""

def translate(words: str) -> str:
    """The phoneme string ``say()`` would use."""
