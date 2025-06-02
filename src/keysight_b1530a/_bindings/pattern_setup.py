from .._ffi import lib
from ..utils import handle_wgfmu_response


@handle_wgfmu_response
def create_pattern(name: str, start_voltage: float) -> None:
    """
    Creates a waveform pattern.

    Args:
        name (str): The name of the pattern to be created.
        start_voltage (float): The starting voltage for the pattern.
    """
    return lib.WGFMU_createPattern(name.encode("utf-8"), start_voltage)


@handle_wgfmu_response
def add_vector(name: str, time_step: float, voltage: float) -> None:
    """
    Specifies a scalar data and connects it to the last point of the specified waveform pattern. This adds a vector to the pattern.

    Execution Conditions:
    Waveform pattern specified by pattern must be created before this function is executed. See `create_pattern` and to create a pattern data.

    Args:
        name (str): The name of the pattern to which the vector will be added.
        time_step (float): Incremental time value, in second. 10-8 (10 ns) to 10995.11627775 seconds, in 10-8 second resolution. If the specified value is out of this range, the vector is not added. If the value is not multiple number of 10 ns, the value is rounded to the nearest multiple number. For example, if the value is 72 ns, the value is rounded to 70 ns.
        voltage (float): Output voltage, in V.
    """
    return lib.WGFMU_addVector(name.encode("utf-8"), time_step, voltage)


@handle_wgfmu_response
def add_vectors(name: str, time_steps: list[float], voltages: list[float]) -> None:
    """
    Specifies a multiple scalar data and connects it to the last point of the specified waveform pattern. This adds vectors to the pattern.

    Execution Conditions:
    Waveform pattern specified by pattern must be created before this function is executed. See `create_pattern` and to create a pattern data.

    Args:
        name (str): The name of the pattern to which the vectors will be added.
        time_steps (list[float]): Incremental time values, in seconds. 10-8 (10 ns) to 10995.11627775 seconds, in 10-8 second resolution. If the specified value is out of this range, the vector is not added. If the value is not multiple number of 10 ns, the value is rounded to the nearest multiple number. For example, if the value is 72 ns, the value is rounded to 70 ns.
        voltages (list[float]): Output voltages, in V.
    """
    if len(time_steps) != len(voltages):
        raise ValueError("time_steps and voltages must have the same length.")

    return lib.WGFMU_addVectors(
        name.encode("utf-8"), time_steps, voltages, len(time_steps)
    )
