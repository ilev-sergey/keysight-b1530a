from .._ffi import ffi, lib
from ..enums import WGFMUMeasureCurrentRange, WGFMUMeasureMode
from ..utils import handle_wgfmu_response
from .config import WGFMUChannel


@handle_wgfmu_response
def execute() -> None:
    """
    Runs the sequencer of all enabled WGFMU channels in the Fast IV mode or the PG mode. The channels start the predefined operation. If there are channels in the run status, this function stops the sequencers and runs the sequencer of all enabled WGFMU channels. After the execution, the channels keep the last output voltage.
    """
    return lib.WGFMU_execute()


@handle_wgfmu_response
def wait_until_completed() -> None:
    """
    Waits until all connected WGFMU channels in the Fast IV mode or the PG mode are in the ready to read data status. Error occurs if a sequencer is not running or if no channel is in the Fast IV mode or the PG mode.
    """
    return lib.WGFMU_waitUntilCompleted()


@handle_wgfmu_response
def connect(channel: WGFMUChannel = WGFMUChannel.CH1) -> None:
    """
    Enables the output of the specified WGFMU channel and the RSU connected to the WGFMU.

    Args:
        channel (WGFMUChannel): The channel to enable.
    """
    return lib.WGFMU_connect(channel)


@handle_wgfmu_response
def disconnect(channel: WGFMUChannel = WGFMUChannel.CH1) -> None:
    """
    Enables the output of the specified WGFMU channel and the RSU connected to the WGFMU.

    Args:
        channel (WGFMUChannel): The channel to enable.
    """
    return lib.WGFMU_disconnect(channel)


@handle_wgfmu_response
def set_measure_mode(
    channel: WGFMUChannel = WGFMUChannel.CH1,
    mode: WGFMUMeasureMode = WGFMUMeasureMode.VOLTAGE,
) -> None:
    """
    Sets the measurement mode of the specified WGFMU channel.

    Args:
        channel (WGFMUChannel): The channel to set the measurement mode for.
        mode (WGFMUMeasureMode): The measurement mode to set.
    """
    return lib.WGFMU_setMeasureMode(channel, mode)


@handle_wgfmu_response
def set_measure_current_range(
    channel: WGFMUChannel = WGFMUChannel.CH1,
    range: WGFMUMeasureCurrentRange = WGFMUMeasureCurrentRange.RANGE_10_UA,
) -> None:
    """
    Sets the current measurement range of the specified WGFMU channel.

    Args:
        channel (WGFMUChannel): The channel to set the measurement range for.
        range (WGFMUMeasureCurrentRange): The current measurement range to set.
    """
    return lib.WGFMU_setMeasureCurrentRange(channel, range)


@handle_wgfmu_response
def dc_force_voltage(
    channel: WGFMUChannel = WGFMUChannel.CH1,
    voltage: float = 0.0,
) -> None:
    """
    Starts DC voltage output immediately on the specified channel.

    The channel must already be in the DC operation mode (set via
    set_operation_mode). The output uses the operation mode, force voltage
    range, measure mode, and measure range that have been set for the channel.

    Args:
        channel (WGFMUChannel): The channel to force the voltage on.
        voltage (float): The DC voltage to output, in V.
    """
    return lib.WGFMU_dcforceVoltage(channel, voltage)


@handle_wgfmu_response
def dc_measure_value(channel: WGFMUChannel = WGFMUChannel.CH1) -> float:
    """
    Starts a single voltage or current measurement and returns the result.

    The measured quantity (voltage or current) follows the channel's measure
    mode. The channel must be in the DC operation mode.

    Args:
        channel (WGFMUChannel): The channel to measure on.

    Returns:
        float: The measured value, in V or A depending on the measure mode.
    """
    value_ptr = ffi.new("double *")
    error_code = lib.WGFMU_dcmeasureValue(channel, value_ptr)
    return error_code, value_ptr[0]


@handle_wgfmu_response
def dc_measure_averaged_value(
    channel: WGFMUChannel = WGFMUChannel.CH1,
    points: int = 1,
    interval: int = 1,
) -> float:
    """
    Starts a sampling measurement and returns the averaged result.

    Samples ``points`` values at a spacing of ``interval * 5 ns`` and returns
    their average. The channel must be in the DC operation mode.

    Args:
        channel (WGFMUChannel): The channel to measure on.
        points (int): Number of sampling points, 1 to 65535.
        interval (int): Sampling interval as a multiple of 5 ns, 1 to 65535.

    Returns:
        float: The averaged measured value, in V or A depending on the
            measure mode.
    """
    value_ptr = ffi.new("double *")
    error_code = lib.WGFMU_dcmeasureAveragedValue(channel, points, interval, value_ptr)
    return error_code, value_ptr[0]
