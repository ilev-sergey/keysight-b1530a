"""
Enumeration types for the Keysight B1530A WGFMU instrument.

This module defines various enumeration types used to configure and control the
B1530A WGFMU instrument. These enumerations represent the native constants from
the WGFMU library, providing type safety and better code readability.

The module includes:
- `WGFMUOperationMode`: Operation modes for the WGFMU (DC, FASTIV, PG, SMU)
- `WGFMUMeasureEvent`: Measurement event modes (AVERAGED, RAW)
- `WGFMUMeasureMode`: Measurement modes (VOLTAGE, CURRENT)

Each enumeration value includes detailed documentation about its purpose and usage
constraints directly from the WGFMU instrument's documentation.

Example usage:
    ```python
    from keysight_b1530a.enums import WGFMUOperationMode

    # Set channel to Fast IV mode
    wgfmu.set_operation_mode(1, WGFMUOperationMode.FASTIV)
    ```
"""

from enum import IntEnum


class WGFMUOperationMode(IntEnum):
    """Operation modes for the WGFMU library."""

    DC = 2000
    """
    DC voltage output and voltage or current measurement (VFVM or VFIM)
    """
    FASTIV = 2001
    """
    Fast IV mode. ALWG voltage output and voltage or current measurement (VFVM or VFIM).
    """
    PG = 2002
    """
    PG mode. ALWG voltage output and voltage measurement (VFVM). The output voltage will be divided by the internal 50 Ohm resistor and the load impedance. Faster than the Fast IV mode.
    """
    SMU = 2003
    """
    SMU mode, default setting. For using SMU connected to the RSU.
    """


class WGFMUMeasureEvent(IntEnum):
    """Measurement event modes for the WGFMU library."""

    AVERAGED = 12000
    """
    Averaging data output mode

    Only the averaging result data will be returned and the number of returned data will be `points`.
    """
    RAW = 12001
    """
    Raw data output mode.

    All of the measurement data used for averaging will be returned and the number of returned data will be `points * (1 + int(average/(5 * 1e-9)))`.
    """


class WGFMUMeasureMode(IntEnum):
    """Measurement modes for the WGFMU library."""

    VOLTAGE = 4000
    """
    Voltage measurement mode, default setting. Changing the mode to this mode does not change the current measurement range setting. Available for the Fast IV, PG, and DC operation modes.
    """
    CURRENT = 4001
    """
    Current measurement mode. Changing the mode to this mode changes the voltage measurement range to the 5 V range. Available for the Fast IV and DC operation modes.
    """
