# `data/` — adapters (infrastructure / persistence)

## Purpose

Implements the **ports** defined in `app/ports.py` using **concrete** mechanisms: in-memory dicts, files, SQLite, REST clients, PLC gateways, etc. This is where **how** we store or load data (or talk to external systems) lives.

## What belongs here

- Classes that **implement** `DataSource`, `DataSink`, or future protocols (same method names and types as the port).
- Thin mapping between port types (`Payload`, etc.) and bytes, SQL rows, tags, or HTTP payloads.

## What does not belong here

- Core business rules (those stay in **`model/`**).
- Multi-step workflows that belong in **`app/`** (orchestration stays in the application layer).

## Dependencies

- **May import** `model` types needed to satisfy port signatures.
- **Implements** contracts from `app.ports`; **should not** be imported by `model/`.

## In this repo

- `memory.py` — `InMemoryStore` implementing read/write for the demo.

## Scaling up

Add modules per backend, e.g. `sqlite_store.py`, `opcua_tags.py`, keeping each behind the same port interfaces where possible.
