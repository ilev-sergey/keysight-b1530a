"""
Keysight B1530A WGFMU Python Library

A Python library for controlling the Keysight B1530A Waveform Generator/Fast Measurement Unit (WGFMU).
This library provides high-level Python bindings for the WGFMU C library, enabling precise control
and measurement capabilities for semiconductor device characterization.
"""

from keysight_b1530a._bindings.event_setup import set_measure_event
from keysight_b1530a._bindings.initialization import clear, close_session, get_channel_ids, initialize, open_session
from keysight_b1530a._bindings.measurement import execute, wait_until_completed
from keysight_b1530a._bindings.pattern_setup import add_vector, add_vectors, create_pattern
from keysight_b1530a._ffi import is_available
from keysight_b1530a.wgfmu import WGFMU

__all__ = [
    "WGFMU",
    "is_available",
    "open_session",
    "close_session",
    "get_channel_ids",
    "execute",
    "wait_until_completed",
    "create_pattern",
    "add_vector",
    "add_vectors",
    "set_measure_event",
    "initialize",
    "clear",
]
