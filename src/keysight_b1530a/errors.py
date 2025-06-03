"""
Error handling for the Keysight B1530A WGFMU instrument.

This module provides error code definitions, error handling utilities, and custom exceptions
for the Keysight B1530A WGFMU instrument. It translates numeric error codes returned by
the all functions in the WGFMU library into meaningful Python exceptions with descriptive messages.

The module includes:
- `WGFMUErrorCode`: Enumeration of error codes defined by the WGFMU library
- `WGFMUError`: Exception class for WGFMU-specific errors
- `check_error`: Decorator for automatically checking return values from WGFMU functions

Example usage:
    ```python
    @check_error
    def my_wgfmu_function():
        # If this returns a negative error code, an exception will be raised
        return lib.wgfmu_some_function()
    ```
"""

import functools
from enum import IntEnum
from typing import Any, Callable


class WGFMUErrorCode(IntEnum):
    """Error codes from the WGFMU library."""

    NO_ERROR = 0
    PARAMETER_OUT_OF_RANGE_ERROR = -1
    ILLEGAL_STRING_ERROR = -2
    CONTEXT_ERROR = -3
    FUNCTION_NOT_SUPPORTED_ERROR = -4
    COMMUNICATION_ERROR = -5
    FW_ERROR = -6
    LIBRARY_ERROR = -7
    ERROR = -8
    CHANNEL_NOT_FOUND_ERROR = -9
    PATTERN_NOT_FOUND_ERROR = -10
    EVENT_NOT_FOUND_ERROR = -11
    PATTERN_ALREADY_EXISTS_ERROR = -12
    SEQUENCER_NOT_RUNNING_ERROR = -13
    RESULT_NOT_READY_ERROR = -14
    RESULT_OUT_OF_DATE = -15
    ERROR_CODE_MIN = -9999


class WGFMUStatusCode(IntEnum):
    """Status codes from the WGFMU library."""

    COMPLETED = 10000
    DONE = 10001
    RUNNING = 10002
    ABORT_COMPLETED = 10003
    ABORTED = 10004
    RUNNING_ILLEGAL = 10005
    IDLE = 10006


ERROR_MESSAGES = {
    WGFMUErrorCode.NO_ERROR: "No error.",
    WGFMUErrorCode.PARAMETER_OUT_OF_RANGE_ERROR: "Invalid parameter value was found. It will be out of the range. Set the effective parameter value.",
    WGFMUErrorCode.ILLEGAL_STRING_ERROR: "Invalid string value was found. It will be empty or illegal (pointer). Set the effective string value.",
    WGFMUErrorCode.CONTEXT_ERROR: "Context error was found between relative functions. Set the effective parameter value.",
    WGFMUErrorCode.FUNCTION_NOT_SUPPORTED_ERROR: "Specified function is not supported by this channel. Set the channel id properly.",
    WGFMUErrorCode.COMMUNICATION_ERROR: "IO library error was found.",
    WGFMUErrorCode.FW_ERROR: "Firmware error was found.",
    WGFMUErrorCode.LIBRARY_ERROR: "WGFMU instrument library error was found.",
    WGFMUErrorCode.ERROR: "Unidentified error was found.",
    WGFMUErrorCode.CHANNEL_NOT_FOUND_ERROR: "Specified channel id is not available for WGFMU. Set the channel id properly.",
    WGFMUErrorCode.PATTERN_NOT_FOUND_ERROR: "Unexpected pattern name was specified. Specify the effective pattern name. Or create a new pattern.",
    WGFMUErrorCode.EVENT_NOT_FOUND_ERROR: "Unexpected event name was specified. Specify the effective event name.",
    WGFMUErrorCode.PATTERN_ALREADY_EXISTS_ERROR: "Duplicate pattern name was specified. Specify the unique pattern name.",
    WGFMUErrorCode.SEQUENCER_NOT_RUNNING_ERROR: "Sequencer must be run to execute the specified function. Run the sequencer.",
    WGFMUErrorCode.RESULT_NOT_READY_ERROR: "Measurement is in progress. Read the result data after the measurement is completed.",
    WGFMUErrorCode.RESULT_OUT_OF_DATE: "Measurement result data was deleted by the setup change. The result data must be read before changing the waveform setup or the measurement setup.",
}


class WGFMUError(Exception):
    """Exception raised for WGFMU errors."""

    def __init__(self, code: int):
        self.code = code

        try:
            self.error_enum = WGFMUErrorCode(code)
            self.message = ERROR_MESSAGES.get(
                self.error_enum, f"Unknown error code: {code}"
            )
        except ValueError:
            self.error_enum = None
            self.message = f"Unknown error code: {code}"

        super().__init__(f"WGFMU Error {code}: {self.message}")


def check_error(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator to check for errors in WGFMU function calls.

    This decorator checks the return value of WGFMU function calls for error codes.
    If a negative integer is returned (indicating an error), it raises a WGFMUError
    with the appropriate error message.

    Parameters:
        func (Callable): The function to wrap.

    Returns:
        Callable: Original function result on success (error code 0).

    Raises:
        WGFMUError: When the function returns a negative error code.
    """

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        result = func(*args, **kwargs)

        # Check if result is an error code
        if isinstance(result, int) and result < 0:
            raise WGFMUError(result)

        # For functions that return multiple values where first is error code
        elif isinstance(result, tuple) and isinstance(result[0], int) and result[0] < 0:
            raise WGFMUError(result[0])

        return result

    return wrapper
