# DesignPatternProject

Minimal **ports and adapters** example: `model/` (rules), `app/` (use cases + ports), `data/` (adapters). The sample loads a `Payload`, normalizes its text, writes the result, and prints it.

## Run

From the repository root:

```bash
python main.py
# or
python -m app
```

## Tests

Standard library only (`unittest`):

```bash
python -m unittest discover -s test -v
```

## Documentation

| Doc | Contents |
|-----|----------|
| [docs/architecture.md](docs/architecture.md) | Ports/adapters, dependency rules, how to extend, benefits |
| [docs/model.md](docs/model.md) | `model/` — domain types and pure logic |
| [docs/app.md](docs/app.md) | `app/` — use cases and ports |
| [docs/data.md](docs/data.md) | `data/` — adapters |
| [docs/test.md](docs/test.md) | `test/` — tests |
