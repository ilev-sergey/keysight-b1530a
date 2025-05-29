from .._ffi import lib
from ..utils import handle_wgfmu_response


@handle_wgfmu_response
def add_sequence(channel: int, pattern_name: str, repetitions: int) -> None:
    """
    Specifies a sequence and connects it to the last point of the sequence data set to the specified channel.

    Execution Conditions:
    Waveform pattern specified by pattern must be created before this function is executed. See create_pattern to create a pattern data.

    Args:
        channel (int): The channel to which the sequence will be added.
        pattern_name (str): The name of the pattern to be used in the sequence.
        repetitions (int): The number of times the pattern will be repeated in the sequence.
    """
    return lib.WGFMU_addSequence(channel, pattern_name.encode("utf-8"), repetitions)
