import numpy as np

from .._ffi import ffi, lib
from ..utils import handle_wgfmu_response


@handle_wgfmu_response
def open_session(address: str = "USB1::0x0957::0x0001::0001::0::INSTR") -> None:
    """
    Opens the communication session with the B1500A by using the WGFMU instrument library.

    Args:
        address (str): VISA address of the instrument. Defaults to Keysight B1500A over USB.

    Raises:
        WGFMUError: If the session could not be opened.
    """
    return lib.WGFMU_openSession(address.encode("utf-8"))


@handle_wgfmu_response
def close_session() -> None:
    """
    Closes the session (communication with B1500A) opened by the open_session function.

    Raises:
        WGFMUError: If the session could not be closed.
    """
    return lib.WGFMU_closeSession()


@handle_wgfmu_response
def initialize() -> None:
    """
    Resets all WGFMU channels. Does not clear the software setup information of the instrument library.

    Raises:
        WGFMUError: If initialization fails.
    """
    return lib.WGFMU_initialize()


@handle_wgfmu_response
def self_test() -> None:
    """
    Performs the self-test for the mainframe and all modules

    Raises:
        WGFMUError: If the self-test fails.
    """
    return lib.WGFMU_doSelfTest()


@handle_wgfmu_response
def _get_channel_count_ptr() -> int:
    """
    Retrieves the number of channels available in the instrument.

    Returns:
        int: The number of channels available.
    """

    channel_count_ptr = ffi.new("int *")
    error_code = lib.WGFMU_getChannelIdSize(channel_count_ptr)

    return error_code, channel_count_ptr


@handle_wgfmu_response
def get_channel_ids():
    """
    Reads the channel id of the WGFMU channels installed in the B1500A
    connected to this session.

    Returns:
        tuple: A tuple containing two arrays: times and values.
    """
    channel_count_ptr = _get_channel_count_ptr()

    channel_ids = np.zeros(channel_count_ptr, dtype=int)
    channel_id_ptr = ffi.new("int *")

    error_code = lib.WGFMU_getChannelIds(channel_id_ptr, channel_count_ptr)
    channel_ids = channel_id_ptr[0]

    return error_code, channel_ids
