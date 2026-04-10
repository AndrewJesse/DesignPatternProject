# Application Layer — Ports.
#
# A PORT is an abstract interface that defines how the application layer
# wants to talk to the outside world (database, filesystem, API, etc.).
# Ports live inside the hexagon and belong to the application, NOT to
# the adapters. They depend only on domain objects.
#
# Adapters implement these ports; the application never knows which
# concrete adapter is behind the interface.
from typing import Protocol

from domain.transform import Payload


class PayloadWriter(Protocol):
    def write(self, data: Payload) -> None: ...
