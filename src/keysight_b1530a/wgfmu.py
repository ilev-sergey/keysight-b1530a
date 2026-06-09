from keysight_b1530a._bindings.configuration import set_operation_mode
from keysight_b1530a._bindings.data_retrieval import get_measurement_data, get_voltage_data
from keysight_b1530a._bindings.measurement import (
    connect,
    dc_force_voltage,
    dc_measure_averaged_value,
    dc_measure_value,
    disconnect,
    set_measure_current_range,
    set_measure_mode,
)
from keysight_b1530a._bindings.sequence_setup import add_sequence
from keysight_b1530a.enums import WGFMUMeasureCurrentRange, WGFMUMeasureMode, WGFMUOperationMode


class WGFMU:
    def __init__(self, id):
        self.id = id

    def enable(self) -> None:
        connect(channel=self.id)

    def disable(self) -> None:
        disconnect(channel=self.id)

    def set_operation_mode(self, mode: WGFMUOperationMode) -> None:
        set_operation_mode(channel=self.id, mode=mode)

    def set_measure_mode(self, mode: WGFMUMeasureMode) -> None:
        set_measure_mode(channel=self.id, mode=mode)

    def set_measure_current_range(self, range: WGFMUMeasureCurrentRange) -> None:
        set_measure_current_range(channel=self.id, range=range)

    def dc_force_voltage(self, voltage: float) -> None:
        dc_force_voltage(channel=self.id, voltage=voltage)

    def dc_measure_value(self) -> float:
        return dc_measure_value(channel=self.id)

    def dc_measure_averaged_value(self, points: int, interval: int) -> float:
        return dc_measure_averaged_value(channel=self.id, points=points, interval=interval)

    def add_sequence(self, pattern_name: str, repetitions: int) -> None:
        add_sequence(channel=self.id, pattern_name=pattern_name, repetitions=repetitions)

    def get_measurement_data(self):
        return get_measurement_data(channel=self.id)

    def get_voltage_data(self):
        return get_voltage_data(channel=self.id)

    def __repr__(self) -> str:
        return f"WGFMU({self.id=})"
