# Domain Layer — pure data structures and business rules.
#
# Domain objects model the instrument cluster's core concepts.
# They have ZERO dependencies on ports, adapters, or frameworks.
#
#   domain/  ← depends on nothing
#   application/  ← depends on domain
#   adapters/  ← depends on domain + application
from dataclasses import dataclass


@dataclass
class VehicleSignal:
    """A single vehicle signal reading (e.g. EngineSpeed, CoolantTemp)."""
    name: str = ""
    value: float = 0.0
    unit: str = ""
    timestamp: str | None = None
