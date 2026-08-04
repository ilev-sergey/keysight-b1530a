"""
Foreign Function Interface (FFI) for the Keysight B1530A WGFMU instrument.

This module provides the low-level FFI initialization for accessing the WGFMU C library.
It handles loading the DLL, and making the library functions available to Python code.

The module exposes:
- `lib`: The loaded WGFMU library with all C functions available for calling. This object is used to interact with the underlying C library. Library functions are wrapped in Python-friendly interfaces and available through the _bindings module.
- `ffi`: The CFFI FFI instance for memory management and data conversion
- `is_available`: Whether the DLL was loaded, i.e. whether C functions can be called

Importing this module never fails. If the DLL cannot be loaded, `lib` becomes a
sentinel that raises `WGFMULibraryError` on the first attempt to call a C
function, so pure-Python parts of the package (error handling, enums, tests)
stay usable on machines without the Keysight driver runtime.

Note that a successful load does not imply an instrument is connected: loading
only maps the driver library. Missing hardware surfaces later, when
`WGFMU_openSession` is called.

Note: This module is for internal use by the keysight_b1530a package and typically
should not be imported directly by end users.
"""

import logging
import re
from pathlib import Path
from typing import Any, NoReturn

from cffi import FFI

from keysight_b1530a.errors import WGFMULibraryError


def load_library(header_path: Path, dll_path: Path) -> Any:
    """
    Load the DLL that contains C functions for operating the B1530A device.

    Args:
        header_path: Path to the header file
        dll_path: Path to the DLL file

    Returns:
        Loaded library object
    """
    with open(header_path, "r") as f:
        header = f.read()

    header = preprocess_header(header)

    # Set up CFFI
    ffi = FFI()
    ffi.cdef(header)

    # Load the DLL
    return ffi.dlopen(str(dll_path))


def preprocess_header(header_content: str) -> str:
    """Clean and preprocess the C header content for CFFI."""
    # Remove preprocessor directives
    header_content = re.sub(r"^\s*#.*$", "", header_content, flags=re.MULTILINE)

    # Remove custom calling convention macros
    header_content = header_content.replace("WGFMUAPI", "").replace("_stdcall", "")

    # Remove empty lines
    header_content = "\n".join(line for line in header_content.splitlines() if line.strip())

    return header_content


class _UnavailableLibrary:
    """Stand-in for `lib` used when the DLL could not be loaded.

    Every attribute access raises, so the failure is reported at the first call
    of a C function rather than at import time.
    """

    def __init__(self, error: Exception) -> None:
        self._error = error

    def __getattr__(self, name: str) -> NoReturn:
        raise WGFMULibraryError(
            f"Cannot call {name}: the WGFMU library failed to load from {DLL_FILE} ({self._error}). "
            "The B1530A driver is 64-bit Windows only and requires the Keysight B1500A/WGFMU "
            "instrument library to be installed."
        ) from self._error


logger = logging.getLogger(__name__)

LIBRARY_DIR = Path(__file__).parent / "lib"
HEADER_FILE = LIBRARY_DIR / "wgfmu.h"
DLL_FILE = LIBRARY_DIR / "wgfmu.dll"

lib: Any
try:
    lib = load_library(HEADER_FILE, DLL_FILE)
except Exception as exc:  # noqa: BLE001 - any load failure degrades the same way
    lib = _UnavailableLibrary(exc)
    LIBRARY_AVAILABLE = False
    logger.warning("WGFMU library unavailable: %s", exc)
else:
    LIBRARY_AVAILABLE = True
    logger.info("WGFMU library loaded successfully.")

# Make FFI instance available for further usage
ffi = FFI()


def is_available() -> bool:
    """Return whether the WGFMU driver library was loaded and C functions can be called.

    This reports only that the driver library is usable on this machine. It says
    nothing about whether an instrument is connected, which is determined by
    `open_session`.
    """
    return LIBRARY_AVAILABLE
