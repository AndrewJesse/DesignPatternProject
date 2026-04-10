# Adapter — SQLite signal store.
#
# Implements the SignalWriter port for SQLite persistence.
# This is a "driven" (secondary) adapter: the application drives it
# through the port interface to persist vehicle signals.
from pathlib import Path
import sqlite3

from domain.transform import VehicleSignal

_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS vehicle_signal (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    value REAL NOT NULL,
    unit TEXT NOT NULL,
    timestamp DATETIME NOT NULL
);
"""


class SqliteSignalStore:
    def __init__(self, path: str = "app.db") -> None:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(path)
        self._ensure_schema()

    def _ensure_schema(self) -> None:
        self._conn.executescript(_SCHEMA_SQL)
        self._conn.commit()

    def write(self, signal: VehicleSignal) -> None:
        self._conn.execute(
            "INSERT INTO vehicle_signal (name, value, unit, timestamp) VALUES (?, ?, ?, ?)",
            (signal.name, signal.value, signal.unit, signal.timestamp),
        )
        self._conn.commit()
