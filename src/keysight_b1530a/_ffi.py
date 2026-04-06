"""
Foreign Function Interface (FFI) for the Keysight B1530A WGFMU instrument.

This module provides the low-level FFI initialization for accessing the WGFMU C library.
It handles loading the DLL, and making the library functions available to Python code.

The module exposes:
- `lib`: The loaded WGFMU library with all C functions available for calling. This object is used to interact with the underlying C library. Library functions are wrapped in Python-friendly interfaces and available through the _bindings module.
- `ffi`: The CFFI FFI instance for memory management and data conversion

Note: This module is for internal use by the keysight_b1530a package and typically
should not be imported directly by end users.
"""

import logging
import re
from pathlib import Path
from typing import Any

from cffi import FFI

logger = logging.getLogger(__name__)

LIBRARY_DIR = Path(__file__).parent / "lib"
HEADER_FILE = LIBRARY_DIR / "wgfmu.h"
DLL_FILE = LIBRARY_DIR / "wgfmu.dll"


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
    _ffi = FFI()
    _ffi.cdef(header)

    # Load the DLL
    try:
        return _ffi.dlopen(str(dll_path))
    except OSError as e:
        raise OSError(
            f"Failed to load wgfmu.dll: {e}\n"
            "This usually means Keysight IO Libraries Suite is not installed.\n"
            "Download it from: https://www.keysight.com/find/iosuitedownload"
        ) from e


def preprocess_header(header_content: str) -> str:
    """Clean and preprocess the C header content for CFFI."""
    # Remove preprocessor directives
    header_content = re.sub(r"^\s*#.*$", "", header_content, flags=re.MULTILINE)

    # Remove custom calling convention macros
    header_content = header_content.replace("WGFMUAPI", "").replace("_stdcall", "")

    # Remove empty lines
    header_content = "\n".join(
        line for line in header_content.splitlines() if line.strip()
    )

    return header_content


class _LazyLibrary:
    """Proxy that defers DLL loading until first attribute access."""

    def __init__(self):
        self._lib = None

    def _load(self):
        if self._lib is None:
            self._lib = load_library(HEADER_FILE, DLL_FILE)
            logger.info("WGFMU library loaded successfully.")
        return self._lib

    def __getattr__(self, name):
        if name == "_lib":
            raise AttributeError(name)
        return getattr(self._load(), name)


lib = _LazyLibrary()

# Make FFI instance available for further usage
ffi = FFI()
