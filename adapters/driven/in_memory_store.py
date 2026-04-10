# Adapter — In-memory signal store.
#
# Implements SignalWriter and SignalReader ports using plain lists.
# Used as a test double so that use-case tests run without real I/O.
from domain.transform import VehicleSignal


class InMemorySignalStore:
    def __init__(self) -> None:
        self._signals: list[VehicleSignal] = []

    def write(self, signal: VehicleSignal) -> None:
        self._signals.append(signal)

    def read(self) -> VehicleSignal | None:
        return self._signals[-1] if self._signals else None

    def last(self) -> VehicleSignal:
        return self._signals[-1] if self._signals else VehicleSignal()