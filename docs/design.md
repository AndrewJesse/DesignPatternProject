# Design — ports and adapters

This project uses **ports and adapters** (hexagonal-style) layering so the **domain** stays independent of how data is stored or presented.

## Dependency direction

- **`model/`** — No imports from `app` or `data`. Pure types and functions.
- **`app/`** — Imports `model` and defines **ports** (`Protocol`s). Orchestrates use cases; does not import concrete adapters.
- **`data/`** — Implements ports (e.g. in-memory store). May import `model` types for signatures.
- **`test/`** — Exercises `model` and `app` (and adapters as needed) without production I/O.

Outer layers depend on inner concepts; the center does not depend on frameworks or storage details.

## Ports and adapters

- **Ports** — Abstract interfaces in `app/ports.py` (`DataSource`, `DataSink`). They describe *what* the application needs, not *how* it is done.
- **Adapters** — Concrete implementations in `data/` (and later UI, APIs, PLC drivers) that satisfy those protocols.

Wiring happens at the **composition root** (`app/main.py`, root `main.py`): choose an adapter and pass it into `pipeline.run`.

## Why this shape

- Swap storage or integrations without rewriting core logic.
- Test use cases and domain rules with fakes or in-memory adapters.
- Give large teams a **shared map** of where code belongs (see per-folder guides in this directory).

## Related docs

| Topic | Doc |
|-------|-----|
| `model/` | [model.md](model.md) |
| `app/` | [app.md](app.md) |
| `data/` | [data.md](data.md) |
| `test/` | [test.md](test.md) |
| Run / layout overview | [../doc/README.md](../doc/README.md) |
