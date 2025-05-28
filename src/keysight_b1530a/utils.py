import functools
from collections.abc import Callable
from typing import Any

from .errors import check_error


def strip_success_code(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to transform results from WGFMU function calls."""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        result = func(*args, **kwargs)

        # Transform single success code
        if isinstance(result, int) and result == 0:
            return None

        # Transform tuple with success code as first element
        elif (
            isinstance(result, tuple) and isinstance(result[0], int) and result[0] == 0
        ):
            remaining = result[1:]
            if len(remaining) == 1:
                return remaining[0]
            else:
                return remaining

        return result

    return wrapper


def handle_wgfmu_response(func: Callable[..., Any]) -> Callable[..., Any]:
    """Combined decorator that checks for errors and unwraps successful results.

    - Raises WGFMUError if a negative error code is returned
    - Removes success code (0) from the successful function call results
    """
    return strip_success_code(check_error(func))
