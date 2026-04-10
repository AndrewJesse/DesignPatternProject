# Adapter — Driving (primary) CLI adapter.
#
# A driving adapter sits on the LEFT side of the hexagon: it receives
# user input and DRIVES the application through its use-case API.
# In a real instrument cluster this would be a Qt GUI adapter.
from application.services import record_signal, read_next_signal
from application.ports import SignalWriter, SignalReader


def run(writer: SignalWriter, reader: SignalReader) -> None:
    # Read signals from the data source (e.g. CAN bus)
    print("--- Reading signals from bus ---")
    while (signal := read_next_signal(reader)) is not None:
        record_signal(writer, signal.name, signal.value, signal.unit)
        print(f"  Recorded: {signal.name} = {signal.value} {signal.unit}")
    print("--- Done ---")
