# Integration tests for the SQLite adapter.
#
# Verifies the concrete adapter reads/writes to a real SQLite database.
import os
import tempfile
import unittest

from adapters.driven.sqlite_store import SqliteSignalStore
from domain.transform import VehicleSignal


class TestSqliteSignalStore(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self._tmp.close()
        self.store = SqliteSignalStore(self._tmp.name)

    def tearDown(self) -> None:
        os.unlink(self._tmp.name)

    def test_write_persists_signal(self) -> None:
        signal = VehicleSignal(name="EngineSpeed", value=1200.0, unit="rpm", timestamp="2026-01-01T00:00:00")
        self.store.write(signal)

        cur = self.store._conn.execute("SELECT name, value, unit, timestamp FROM vehicle_signal")
        row = cur.fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row[0], "EngineSpeed")
        self.assertEqual(row[1], 1200.0)
        self.assertEqual(row[2], "rpm")

    def test_write_multiple_signals(self) -> None:
        self.store.write(VehicleSignal(name="EngineSpeed", value=1200.0, unit="rpm", timestamp="2026-01-01T00:00:00"))
        self.store.write(VehicleSignal(name="CoolantTemp", value=92.5, unit="°C", timestamp="2026-01-01T00:00:01"))

        cur = self.store._conn.execute("SELECT COUNT(*) FROM vehicle_signal")
        self.assertEqual(cur.fetchone()[0], 2)


if __name__ == "__main__":
    unittest.main()
