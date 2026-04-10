# Adapter — Mock CAN bus signal reader.
#
# Implements the SignalReader port with hardcoded vehicle signals.
# Simulates reading from a CAN bus without real hardware.
# In production this would be replaced by a real CAN adapter
# (e.g. using python-can, Vector CANoe, or SocketCAN).
from domain.transform import VehicleSignal

_MOCK_SIGNALS = [
    VehicleSignal(name="EngineSpeed", value=1200.0, unit="rpm"),
    VehicleSignal(name="CoolantTemp", value=92.5, unit="°C"),
    VehicleSignal(name="VehicleSpeed", value=65.0, unit="km/h"),
]


class MockCANReader:
    def __init__(self) -> None:
        self._index = 0

    def read(self) -> VehicleSignal | None:
        if self._index >= len(_MOCK_SIGNALS):
            return None
        signal = _MOCK_SIGNALS[self._index]
        self._index += 1
        return signal
