import numpy as np

from .._ffi import ffi, lib
from ..utils import handle_wgfmu_response
from .config import WGFMUChannel


@handle_wgfmu_response
def _get_measurement_data_size(channel: WGFMUChannel = WGFMUChannel.CH1) -> int:
    """
    Retrieves the size of the measurement data for the specified channel.

    Args:
        channel (WGFMUChannel): The channel to retrieve data size from. Defaults to CH1.

    Returns:
        int: The number of data points available in the measurement.
    """

    measured_size_ptr = ffi.new("int *")
    total_size_ptr = ffi.new("int *")
    error_code = lib.WGFMU_getMeasureValueSize(
        channel, measured_size_ptr, total_size_ptr
    )
    return error_code, measured_size_ptr[0]


@handle_wgfmu_response
def get_measurement_data(channel: WGFMUChannel = WGFMUChannel.CH1) -> int:
    """
    Retrieves the measurement data (voltage or current depending on the measure mode) from the specified channel.

    Args:
        channel (WGFMUChannel): The channel to retrieve data from. Defaults to CH1.

    Returns:
        tuple: A tuple containing two arrays: times and values (voltages or currents).
    """
    num_points = _get_measurement_data_size(channel)

    times = np.zeros(num_points)
    values = np.zeros(num_points)

    time_ptr = ffi.new("double *")
    value_ptr = ffi.new("double *")

    for i in range(num_points):
        error_code = lib.WGFMU_getMeasureValue(channel, i, time_ptr, value_ptr)
        times[i] = time_ptr[0]
        values[i] = value_ptr[0]

    return error_code, times, values
