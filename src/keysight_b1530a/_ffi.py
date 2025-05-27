import logging
import re
from pathlib import Path
from typing import Any

from cffi import FFI


def load_library(header_path: Path, dll_path: Path) -> Any:
    """
    Load the WGFMU library using CFFI.

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
    header_content = "\n".join(
        line for line in header_content.splitlines() if line.strip()
    )

    return header_content


logger = logging.getLogger(__name__)

LIBRARY_DIR = Path(__file__).parent / "lib"
HEADER_FILE = LIBRARY_DIR / "wgfmu.h"
DLL_FILE = LIBRARY_DIR / "wgfmu.dll"

lib = load_library(HEADER_FILE, DLL_FILE)

# Make FFI instance available for further usage
ffi = FFI()

logger.info("WGFMU library loaded successfully.")
