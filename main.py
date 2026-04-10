# Composition Root (aka "main" or "bootstrap").
#
# The ONLY place that knows about concrete adapters.
# Wires a driven SignalReader (mock CAN bus) and a driven SignalWriter
# (SQLite store) to the driving adapter (CLI).
#
# In Ports & Adapters, the composition root sits OUTSIDE the hexagon.
from adapters.driven.sqlite_store import SqliteSignalStore
from adapters.driven.mock_can_reader import MockCANReader
from adapters.driving.cli import run as run_cli


def main() -> None:
    writer = SqliteSignalStore("data/signals.db")  # driven adapter (right side)
    reader = MockCANReader()                        # driven adapter (right side)
    run_cli(writer, reader)                         # driving adapter (left side)


if __name__ == "__main__":
    main()
