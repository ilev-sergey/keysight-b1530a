import numpy as np

from .._ffi import ffi, lib
from ..utils import handle_wgfmu_response, strip_error_code


@strip_error_code  # doesn't use check_error in order not to raise an error if the session is already opened
def open_session(address: str = "USB1::0x0957::0x0001::0001::0::INSTR") -> None:
    """
    Opens the communication session with the B1500A by using the WGFMU instrument library.

    Args:
        address (str): VISA address of the instrument. Defaults to Keysight B1500A over USB.
    """
    return lib.WGFMU_openSession(address.encode("utf-8"))


@handle_wgfmu_response
def close_session() -> None:
    """
    Closes the session (communication with B1500A) opened by the open_session function.
    """
    return lib.WGFMU_closeSession()


@handle_wgfmu_response
def initialize() -> None:
    """
    Resets all WGFMU channels. Does not clear the software setup information of the instrument library.
    """
    return lib.WGFMU_initialize()


@handle_wgfmu_response
def clear() -> None:
    """
    Clears the instrument library’s software setup information such as all pattern and sequence information, error, error summary, warning, warning summary, warning level, warning level for the `treat_warnings_as_errors` function.
    """
    return lib.WGFMU_clear()


@handle_wgfmu_response
def self_test() -> None:
    """
    Performs the self-test for the mainframe and all modules.
    """
    return lib.WGFMU_doSelfTest()


@handle_wgfmu_response
def _get_channel_count_ptr() -> int:
    """
    Returns the number of WGFMU channels installed in the B1500A connected to this session.

    Returns:
        tuple: A pointer to an integer that will hold the number of WGFMU channels.
    """

    channel_count_ptr = ffi.new("int *")
    error_code = lib.WGFMU_getChannelIdSize(channel_count_ptr)

    return error_code, channel_count_ptr


@handle_wgfmu_response
def get_channel_ids():
    """
    Reads the channel id of the WGFMU channels installed in the B1500A connected to this session.

    Returns:
        list(int): List of channel IDs.
    """
    channel_count_ptr = _get_channel_count_ptr()
    channel_ids_ptr = ffi.new("int[]", channel_count_ptr[0])

    error_code = lib.WGFMU_getChannelIds(channel_ids_ptr, channel_count_ptr)

    return error_code, list(channel_ids_ptr)
