import pytest

from keysight_b1530a.errors import ERROR_MESSAGES, WGFMUError, check_error
from keysight_b1530a.utils import handle_wgfmu_response


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


@pytest.mark.parametrize(
    "result, expected",
    [
        (0, None),  # Single success code
        ((0, 1), 1),  # Tuple with success code and one additional value
        ((0, 1, 2), (1, 2)),  # Tuple with success code and multiple values
        ((0, [1, 2]), [1, 2]),  # Tuple with success code and a list
        ((0, "data"), "data"),  # Tuple with success code and string data
    ],
)
def test_success_handling(result, expected):
    """Test successful handling of function results."""

    @handle_wgfmu_response
    def successful_function():
        return result

    assert successful_function() == expected
