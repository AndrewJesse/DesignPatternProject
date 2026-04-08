# `test/` — automated tests

## Purpose

Verifies **`model`** and **`app`** behavior **without** requiring real hardware, production databases, or manual steps. Keeps refactors safe as the team and codebase grow.

## What belongs here

- **Unit tests** for pure functions and small units (e.g. `test_transform.py` for `normalize`).
- **Integration-style tests** that run the pipeline with test doubles or in-memory adapters (e.g. `test_pipeline.py` with `InMemoryStore`).

## What does not belong here

- Production configuration or secrets.
- Long, flaky tests that depend on external services unless isolated behind CI with clear labels.

## Conventions

- Test files are named `test_*.py` so pytest discovers them.
- Pytest configuration lives in the root **`pyproject.toml`** (`[tool.pytest.ini_options]`) for this repo.

## Dependencies

- Tests **import** the same packages as production code (`model`, `app`, `data`) and assert on behavior, not private internals when avoidable.
