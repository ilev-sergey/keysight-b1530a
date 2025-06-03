from enum import IntEnum


class WGFMUChannel(IntEnum):
    """Channel IDs for the WGFMU library.

    This enum should contain the channels that are available in the B1500A. Channel IDs depend on the connection of your instrument to the measurement unit. The values should be adjusted. Most functions will use the channel `CH1` by default if no channel is specified."""

    CH1 = 201
    """Channel 1 of the WGFMU installed in the slot 2"""
    CH2 = 202
    """Channel 2 of the WGFMU installed in the slot 2"""
    CH3 = 301
    """Channel 3 of the WGFMU installed in the slot 3"""
