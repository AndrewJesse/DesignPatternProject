# Unit tests for the application layer (use cases).
#
# Tests core business logic by plugging in the InMemorySignalStore,
# so no real I/O occurs.
import unittest

from adapters.driven.in_memory_store import InMemorySignalStore
from adapters.driven.mock_can_reader import MockCANReader
from application.services import record_signal, read_next_signal


class TestRecordSignal(unittest.TestCase):
    def test_records_signal_with_trimmed_name(self) -> None:
        store = InMemorySignalStore()
        saved = record_signal(store, "  EngineSpeed  ", 1200.0, "rpm")
        self.assertEqual(saved.name, "EngineSpeed")
        self.assertEqual(saved.value, 1200.0)
        self.assertIsNotNone(saved.timestamp)
        self.assertEqual(store.last().name, "EngineSpeed")


class TestReadNextSignal(unittest.TestCase):
    def test_reads_signals_from_reader(self) -> None:
        reader = MockCANReader()
        first = read_next_signal(reader)
        self.assertIsNotNone(first)
        self.assertEqual(first.name, "EngineSpeed")

    def test_returns_none_when_exhausted(self) -> None:
        reader = MockCANReader()
        for _ in range(10):
            read_next_signal(reader)
        self.assertIsNone(read_next_signal(reader))


if __name__ == "__main__":
    unittest.main()
