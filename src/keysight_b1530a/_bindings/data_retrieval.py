from webbrowser import get

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

    return error_code, np.array(times), np.array(values)


@handle_wgfmu_response
def get_voltage_value(
    channel: WGFMUChannel = WGFMUChannel.CH1, time: float = 0.0
) -> float:
    """
    Retrieves the voltage value at a specific time from the specified channel.

    Args:
        channel (WGFMUChannel): The channel to retrieve data from. Defaults to CH1.
        time (float): The time at which to retrieve the voltage value. Defaults to 0.0.

    Returns:
        float: The voltage value at the specified time.
    """
    value_ptr = ffi.new("double *")
    error_code = lib.WGFMU_getInterpolatedForceValue(channel, time, value_ptr)
    return error_code, value_ptr[0]


@handle_wgfmu_response
def get_voltage_data(channel: WGFMUChannel = WGFMUChannel.CH1):
    times, _ = get_measurement_data(channel)
    voltages = [get_voltage_value(channel, time) for time in times]
    return np.array(voltages)


@handle_wgfmu_response
def export_measurement_setup(
    filename: str = "measurement_setup.csv",
) -> None:
    """
    This function creates a setup summary report and saves it as a csv (comma separated
    values) file.

    The summary report contains the pattern data, event data, and sequence
    data for the channels configured by the instrument library. The file can be read by
    using a spreadsheet software. This is effective for quick debugging. See Figure 4-1
    for example data.

    If the specified file does not exist, this function creates new file. If the specified file
    exists, this function overwrites the file. Error occurs if an invalid path is specified, a
    file is not created, or a setup summary is not written.

    Args:
        filename (str): Name of the summary report file. Defaults to "measurement_setup.csv".
    """
    return lib.WGFMU_exportAscii(filename.encode("utf-8"))
