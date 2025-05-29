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
