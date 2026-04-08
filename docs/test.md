# `test/` — automated tests

## Purpose

Verifies **`model`** and **`app`** behavior **without** requiring real hardware, production databases, or manual steps.

## What belongs here

- **Unit tests** for pure functions (e.g. `test_transform.py`).
- **Integration-style tests** that run the pipeline with in-memory adapters (e.g. `test_pipeline.py`).

## Conventions

- Tests use the standard library **`unittest`** module (no extra test runner dependency).
- Run from the repo root:

  ```bash
  python -m unittest discover -s test -v
  ```

## Dependencies

- Tests import the same packages as production code (`model`, `app`, `data`). Run with the working directory set to the **project root** so those packages resolve.
