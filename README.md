# HMI Instrument Cluster — Hexagonal Architecture

Ports & Adapters scaffold for a vehicle instrument cluster.
Two ports (`SignalWriter`, `SignalReader`), three driven adapters
(SQLite, in-memory, mock CAN bus), one driving adapter (CLI),
and a composition root that wires them together.

> Open **[architecture.html](architecture.html)** in a browser for an
> interactive hexagon diagram.

## Project structure

```
HexagonalArchitecture/
    domain/                              # Innermost — depends on nothing
        transform.py                     #   VehicleSignal dataclass
    application/                         # Middle — depends on domain only
        ports/                           #   Port interfaces (Protocols)
            ports.py                     #     SignalWriter, SignalReader
        services/                        #   Use cases / orchestration
            memo_use_cases.py            #     record_signal(), read_next_signal()
            tests/
                test_write_user_input.py #     Use case tests (in-memory mock)
    adapters/                            # Outermost — depends on domain + application
        driving/                         #   LEFT side (primary) — drives the app
            cli.py                       #     CLI adapter
            tests/
                test_cli.py              #     CLI adapter tests
        driven/                          #   RIGHT side (secondary) — app drives these
            in_memory_store.py           #     Test double (SignalWriter + SignalReader)
            sqlite_store.py              #     Real persistence (SignalWriter)
            mock_can_reader.py           #     Simulated CAN bus (SignalReader)
            tests/
                test_sqlite_store.py     #     SQLite adapter tests
    main.py                              # Composition root — wires everything
    __main__.py                          # Entry point: python -m HexagonalArchitecture
    architecture.html                    # Visual hexagon diagram (open in browser)
    example/                             # Standalone demo scripts
        with_hexagonal.py                #   Discount calculator (hexagonal)
        without_hexagonal.py             #   Discount calculator (no hexagonal)
```

## Run

```bash
python3 main.py
```

## Tests

```bash
python3 -m pytest adapters/driven/tests/ adapters/driving/tests/ application/services/tests/ -v
```

## Architecture

Based on Alistair Cockburn's Hexagonal Architecture (2005) combined with
Clean Architecture layering. Framed around an instrument cluster domain:
vehicle signals flow in from a CAN bus (driven adapter), get processed by
use cases, and are persisted to a signal store (driven adapter).

### Dependency direction

```
domain/        ← depends on nothing
application/   ← depends on domain
adapters/      ← depends on domain + application
main.py        ← depends on everything (wiring only)
```

Dependencies flow **inward**. The center never imports from outer layers.

### Ports and adapters

- **Ports** — Abstract interfaces in `application/ports/`:
  - `SignalWriter` — persist or forward a vehicle signal.
  - `SignalReader` — read the next signal from a data source.
- **Driving adapters** (primary, left side) — Things that call INTO the
  application: `adapters/driving/cli.py`, test harnesses.
- **Driven adapters** (secondary, right side) — Things the application calls
  OUT to: `SqliteSignalStore`, `InMemorySignalStore`, `MockCANReader`.
- **Composition root** — `main.py` wires concrete adapters to ports.

### Why this shape

- Swap the mock CAN reader for a real SocketCAN adapter — no core changes.
- Swap SQLite for a time-series DB — only one adapter to replace.
- Test use cases with in-memory adapters — no hardware, no database.
- Replace CLI with a Qt GUI adapter — the application layer stays untouched.

## Folder guide

### `domain/` — domain model and pure logic

**Purpose:** Types that express business rules with no I/O.

**What belongs here:** `VehicleSignal`, gauge thresholds, alarm rules.

**What does not belong:** Imports from `application/` or `adapters/`. Any I/O.

### `application/` — use cases and ports

**Purpose:** Orchestrates what the system does. Defines ports as abstract interfaces.

- `ports/` — `SignalWriter`, `SignalReader` Protocols.
- `services/` — `record_signal()`, `read_next_signal()`.

**What does not belong:** Concrete I/O implementations (those live in `adapters/`).

### `adapters/` — infrastructure (outside the hexagon)

**Purpose:** Implements ports with concrete technology.

- `driving/` — Primary adapters that **drive** the application (CLI, Qt GUI, HTTP, test harnesses).
- `driven/` — Secondary adapters that the application **drives** (databases, CAN bus, file systems).

### `main.py` — composition root

The only file that knows about concrete adapters. Wires them together
and starts the program. No business logic.

## How to add code and keep separation

1. **New domain concept** (e.g. `DTCAlert`) → `domain/`.
2. **New use case** (e.g. `check_alarm_thresholds`) → `application/services/`.
3. **New data source** (e.g. real CAN bus) → implement `SignalReader` in `adapters/driven/`.
4. **New output** (e.g. Qt gauge display) → implement `SignalWriter` in `adapters/driving/`.
5. **Wire it** → update `main.py`.
