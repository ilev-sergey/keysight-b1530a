import pytest

from keysight_b1530a import is_available
from keysight_b1530a._ffi import _UnavailableLibrary
from keysight_b1530a.errors import WGFMULibraryError


def test_import_reports_availability():
    """Importing the package always works and reports whether the DLL loaded."""
    assert isinstance(is_available(), bool)


def test_unavailable_library_raises_on_call():
    """Without a usable DLL, touching a C function raises a descriptive error."""
    cause = OSError("cannot load library")
    lib = _UnavailableLibrary(cause)

    with pytest.raises(WGFMULibraryError) as excinfo:
        _ = lib.WGFMU_openSession

    assert "WGFMU_openSession" in str(excinfo.value)
    assert "wgfmu.dll" in str(excinfo.value)
    assert excinfo.value.__cause__ is cause
