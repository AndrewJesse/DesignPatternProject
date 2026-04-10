# Tests for the driving CLI adapter.
#
# Verifies the CLI adapter reads signals from mock CAN bus,
# records them, and prints output — without real I/O.
import unittest
from io import StringIO
from unittest.mock import patch

from adapters.driven.in_memory_store import InMemorySignalStore
from adapters.driven.mock_can_reader import MockCANReader
from adapters.driving.cli import run


class TestCliAdapter(unittest.TestCase):
    @patch("sys.stdout", new_callable=StringIO)
    def test_run_reads_and_records_signals(self, mock_stdout):
        store = InMemorySignalStore()
        reader = MockCANReader()
        run(store, reader)
        # Should have recorded all 3 mock signals
        self.assertEqual(store.last().name, "VehicleSpeed")
        output = mock_stdout.getvalue()
        self.assertIn("EngineSpeed", output)
        self.assertIn("Done", output)


if __name__ == "__main__":
    unittest.main()
