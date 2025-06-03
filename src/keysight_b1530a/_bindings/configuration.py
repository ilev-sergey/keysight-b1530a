from .._ffi import lib
from ..enums import WGFMUOperationMode
from ..utils import handle_wgfmu_response
from .config import WGFMUChannel


@handle_wgfmu_response
def set_operation_mode(
    channel: WGFMUChannel = WGFMUChannel.CH1,
    mode: WGFMUOperationMode = WGFMUOperationMode.FASTIV,
) -> None:
    """
    Sets the operation mode of the specified channel. The setting is applied to the channel by the `update`, `update_channel`, `execute`, or the functions of the DC measurement group.

    Args:
        channel (WGFMUChannel): The channel to set the operation mode for.
        mode (WGFMUOperationMode): The operation mode to set.
    """
    return lib.WGFMU_setOperationMode(channel, mode)
