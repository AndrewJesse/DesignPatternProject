# Application Layer — Ports.
#
# Ports are abstract interfaces at the hexagon boundary.
# They define WHAT the application needs, not HOW it's done.
# Adapters implement these; the application never knows which
# concrete adapter is behind the interface.
from typing import Protocol

from domain.transform import VehicleSignal


class SignalWriter(Protocol):
    """Driven port — persist or forward a vehicle signal."""
    def write(self, signal: VehicleSignal) -> None: ...


class SignalReader(Protocol):
    """Driven port — read the next vehicle signal from a data source."""
    def read(self) -> VehicleSignal | None: ...
