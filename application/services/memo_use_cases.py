# Application Layer — Use Cases (Services).
#
# Use cases orchestrate the flow of data to and from domain entities
# through ports.  They answer "WHAT does the app do?" but not "HOW
# is data stored or read?" — that detail is behind the port.
from datetime import datetime

from ..ports import SignalWriter, SignalReader
from domain.transform import VehicleSignal


def record_signal(writer: SignalWriter, name: str, value: float, unit: str) -> VehicleSignal:
    """Accept a signal reading and persist it through the writer port."""
    signal = VehicleSignal(
        name=name.strip(),
        value=value,
        unit=unit.strip(),
        timestamp=datetime.now().isoformat(timespec="seconds"),
    )
    writer.write(signal)
    return signal


def read_next_signal(reader: SignalReader) -> VehicleSignal | None:
    """Read the next available signal from the reader port."""
    return reader.read()
