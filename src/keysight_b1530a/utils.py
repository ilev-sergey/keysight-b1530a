"""
Utility functions for WGFMU library function call handling.

This module provides decorators to simplify interaction with the WGFMU C library by handling common patterns like error checking and result unwrapping.

Example usage:
    ```python
    @handle_wgfmu_response
    def some_wgfmu_function(param1, param2):
        # This function returns (error_code, actual_data)
        return _raw_wgfmu_call(param1, param2)

    # Usage - only returns actual_data, raises exception on error
    data = some_wgfmu_function(1, 2)
    ```
"""

import functools
from collections.abc import Callable
from typing import Any

from .errors import check_error


def strip_error_code(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator to transform results from WGFMU function calls by removing success codes.

    This decorator handles the common WGFMU pattern where successful function calls
    return either:
    - A single integer (0 for success) - transformed to None
    - A tuple with success code as first element - success code removed

    Args:
        func: The function to wrap. Should return either an int or tuple where
              the first element is an integer error/success code.

    Returns:
        A wrapped function that returns cleaned results without success codes.

    Examples:
        ```python
        @strip_error_code
        def get_data():
            return (0, "actual_data")  # Success code + data

        result = get_data()  # Returns "actual_data"

        @strip_error_code
        def simple_command():
            return 0  # Just success code

        result = simple_command()  # Returns None
        ```

    Note:
        This decorator should typically be used together with check_error()
        to ensure error codes are handled before being stripped.
    """

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        result = func(*args, **kwargs)

        # Transform single success code (0) to None
        if isinstance(result, int):
            return None

        # Transform tuple with success code as first element
        elif isinstance(result, tuple) and isinstance(result[0], int):
            remaining = result[1:]
            # Single remaining element - return it directly
            if len(remaining) == 1:
                return remaining[0]
            # Multiple remaining elements - return as tuple
            else:
                return remaining

        # Return unchanged if not matching expected patterns
        return result

    return wrapper


def handle_wgfmu_response(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Combined decorator that provides complete WGFMU response handling.

    This decorator combines error checking and result unwrapping in the correct order:
    1. First checks for error codes and raises WGFMUError if found
    2. Then strips success codes from the result

    This is the recommended decorator for most WGFMU binding functions as it
    provides the cleanest Python interface - functions either return useful data
    or raise meaningful exceptions.

    Args:
        func: The WGFMU binding function to wrap. Should return either:
              - An integer error/success code
              - A tuple with error/success code as first element

    Returns:
        A wrapped function that returns cleaned data or raises WGFMUError.

    Raises:
        WGFMUError: If the wrapped function returns a negative error code.

    Examples:
        ```python
        @handle_wgfmu_response
        def get_channel_count():
            # Raw call returns (error_code, count)
            return wgfmu_lib.wgfmu_getChannelCount()

        # Clean usage - returns count or raises exception
        count = get_channel_count()

        @handle_wgfmu_response
        def initialize_instrument():
            # Raw call returns just error_code
            return wgfmu_lib.wgfmu_initialize()

        # Clean usage - returns None or raises exception
        initialize_instrument()
        ```

    Note:
        This decorator is equivalent to applying @strip_error_code and @check_error
        in the correct order, but is more convenient.
    """
    return strip_error_code(check_error(func))
