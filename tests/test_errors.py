import pytest

from keysight_b1530a.errors import ERROR_MESSAGES, WGFMUError, check_error


@pytest.mark.parametrize(
    "error_code, expected_message",
    [
        (-1, ERROR_MESSAGES.get(-1)),  # Error code -1 maps to enum 1
        (-15, ERROR_MESSAGES.get(-15)),  # Error code -15 maps to enum 15
        (
            -999,
            "Unknown error code: -999",  # Assuming unknown error codes have a default message
        ),
    ],
)
def test_error_handling(error_code, expected_message):
    """Test error handling with different error codes."""

    @check_error
    def faulty_function():
        # Simulate an error by returning the specified error code
        return error_code

    with pytest.raises(WGFMUError) as excinfo:
        faulty_function()

    assert excinfo.value.code == error_code
    assert str(excinfo.value) == f"WGFMU Error {error_code}: {expected_message}"
