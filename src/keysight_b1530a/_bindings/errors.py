from .._ffi import ffi, lib
from ..utils import handle_wgfmu_response


@handle_wgfmu_response
def get_error_detail() -> str:
    """Get detailed error information from the WGFMU library."""
    # Get error summary size
    size_ptr = ffi.new("int*")
    error_code = lib.WGFMU_getErrorSummarySize(size_ptr)
    size = size_ptr[0]

    if size > 0:
        # Allocate buffer and get error summary
        buffer = ffi.new(f"char[{size}]")
        lib.WGFMU_getErrorSummary(buffer, size_ptr)
        return error_code, ffi.string(buffer).decode("utf-8")
    return error_code, "No error details available"
