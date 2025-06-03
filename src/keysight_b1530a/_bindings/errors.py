from .._ffi import ffi, lib
from ..utils import strip_error_code


@strip_error_code
def get_error_summary() -> str:
    """Reads the error summary string which contains all errors. Useful when something goes wrong. The string is cleared by the `initialization.clear` function.

    Returns:
        str: A string containing the error code, description and additional information. If no errors are found, it returns "No errors found."
    """
    size_ptr = ffi.new("int*")
    error_code = lib.WGFMU_getErrorSummarySize(size_ptr)
    size = size_ptr[0]

    if size > 0:
        buffer = ffi.new(f"char[{size}]")
        lib.WGFMU_getErrorSummary(buffer, size_ptr)
        return error_code, ffi.string(buffer).decode("utf-8")

    return error_code, "No errors found."
