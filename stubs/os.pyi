"""Files in the board's flash filesystem (flat, no directories). Flashing firmware erases them."""

from typing import List, NamedTuple

class _UName(NamedTuple):
    sysname: str
    nodename: str
    release: str
    version: str
    machine: str

def listdir() -> List[str]:
    """Names of all files."""

def remove(filename: str) -> None:
    """Delete a file."""

def size(filename: str) -> int:
    """Size of a file in bytes."""

def uname() -> _UName:
    """Firmware and board version information."""
