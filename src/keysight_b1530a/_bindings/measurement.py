from .._ffi import lib
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
