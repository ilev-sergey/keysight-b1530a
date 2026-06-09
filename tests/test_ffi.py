from unittest.mock import patch

import pytest

from keysight_b1530a._ffi import _LazyLibrary


def test_lazy_library_not_loaded_on_init():
    """DLL should not be loaded when _LazyLibrary is created."""
    lazy = _LazyLibrary()
    assert lazy._lib is None


def test_lazy_library_loads_on_access():
    """DLL should load on first attribute access."""
    lazy = _LazyLibrary()
    sentinel = type("FakeLib", (), {"some_function": 42})()
    with patch("keysight_b1530a._ffi.load_library", return_value=sentinel) as mock_load:
        result = lazy.some_function
        assert result == 42
        assert lazy._lib is sentinel
        mock_load.assert_called_once()


def test_lazy_library_caches_after_load():
    """DLL should only be loaded once, even with multiple attribute accesses."""
    lazy = _LazyLibrary()
    sentinel = type("FakeLib", (), {"a": 1, "b": 2})()
    with patch("keysight_b1530a._ffi.load_library", return_value=sentinel) as mock_load:
        _ = lazy.a
        _ = lazy.b
        mock_load.assert_called_once()


def test_load_library_clear_error_message():
    """When DLL fails to load, error should mention Keysight IO Libraries download URL."""
    lazy = _LazyLibrary()
    with patch("cffi.FFI.dlopen", side_effect=OSError("error 0x7e")):
        with pytest.raises(OSError, match="Keysight IO Libraries Suite"):
            _ = lazy.some_function
