from .._ffi import lib
from ..enums import WGFMUMeasureEvent
from ..utils import handle_wgfmu_response


@handle_wgfmu_response
def set_measure_event(
    pattern_name: str,
    event_name: str,
    points: int,
    interval: float,
    average: float,
    mode: WGFMUMeasureEvent = WGFMUMeasureEvent.AVERAGED,
    start_time: float = 0.0,
) -> None:
    """
    Defines a measurement event which is a sampling measurement performed by the WGFMU channel while it outputs a waveform pattern.

    Execution Conditions:
    Waveform pattern specified by pattern must be created before this function is executed. See `create_pattern` to create a pattern data.

    Args:
        pattern_name (str): Name of the waveform pattern. The measurement event is performed while the WGFMU channel outputs this waveform pattern.
        event_name (str): Measurement event name.
        start_time (float): Start time of the measurement event, in seconds.

            Sampling measurement is started at this time. Time origin is the origin of the specified pattern. The sampling measurement will be stopped at the following `eventEndTime`. If you set `average`=0, add 1e-8 (10 ns) to the formula.

            `eventEndTime` = `start_time` + `interval` * (points - 1) + `average`

            The time and `eventEndTime` must be 0 to the total time of pattern in 1e-8 (10 ns) resolution.
    """
    return lib.WGFMU_setMeasureEvent(
        pattern_name.encode("utf-8"),
        event_name.encode("utf-8"),
        start_time,
        points,
        interval,
        average,
        mode,
    )
