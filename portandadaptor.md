# Port and Adapter Pattern — Minimal Example

## With Port and Adapter

```python
import psycopg2
from abc import ABC, abstractmethod


# --- Port (interface) ---
class UserRepository(ABC):
    @abstractmethod
    def get_user(self, user_id: int) -> dict:
        ...


# --- Adapter (swappable implementation) ---
class PostgresUserRepository(UserRepository):
    def __init__(self, connection_string: str):
        self.connection_string = connection_string

    def get_user(self, user_id: int) -> dict:
        conn = psycopg2.connect(self.connection_string)
        cur = conn.cursor()
        cur.execute("SELECT name FROM users WHERE id = %s", (user_id,))
        name = cur.fetchone()[0]
        cur.close()
        conn.close()
        return {"id": user_id, "name": name}


# --- Core domain logic (depends only on the port) ---
class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def greet(self, user_id: int) -> str:
        user = self.repo.get_user(user_id)
        return f"Hello, {user['name']}!"


# --- Usage ---
repo = PostgresUserRepository("dbname=mydb user=admin password=secret")
service = UserService(repo)
print(service.greet(1))


# --- Test (no database needed) ---
class FakeUserRepository(UserRepository):
    def get_user(self, user_id: int) -> dict:
        return {"id": user_id, "name": "Alice"}


def test_greet():
    service = UserService(FakeUserRepository())
    assert service.greet(1) == "Hello, Alice!"
```

**What's happening:**
- `UserRepository` is the **port** — a contract your core logic codes against.
- `PostgresUserRepository` is the **adapter** — a plug-in implementation you can swap without touching `UserService`.
- `UserService` never knows *how* data is fetched, only *that* it can be.
- To test, you create a tiny fake adapter that returns canned data — no DB, no mocking library, instant.

---

## Without Port and Adapter (same feature)

```python
import psycopg2


class UserService:
    def greet(self, user_id: int) -> str:
        conn = psycopg2.connect("dbname=mydb user=admin password=secret")
        cur = conn.cursor()
        cur.execute("SELECT name FROM users WHERE id = %s", (user_id,))
        name = cur.fetchone()[0]
        cur.close()
        conn.close()
        return f"Hello, {name}!"


service = UserService()
print(service.greet(1))


# --- Test (requires mocking the DB) ---
from unittest.mock import patch, MagicMock


def test_greet():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = ("Alice",)
    mock_conn.cursor.return_value = mock_cursor

    with patch("psycopg2.connect", return_value=mock_conn):
        service = UserService()
        assert service.greet(1) == "Hello, Alice!"
```

---

## Why the first version is better

| Concern | With Port & Adapter | Without |
|---|---|---|
| **Testing** | Write a second adapter with canned data, inject it — no DB needed | Must mock `psycopg2` or spin up a real database |
| **Swapping storage** | Add a new adapter class, change one line | Rewrite every method that touches the DB |
| **Readability** | `UserService` contains only business logic | Business logic is tangled with connection strings and SQL |
| **Credentials** | Adapter owns connection details | Hardcoded in business logic |
| **Runtime speed** | Identical (one extra method call = nanoseconds; the DB query = milliseconds) | Identical |
| **Test speed** | Instant — no DB, no mocking library | Slower — needs mock setup or a real DB |

---

## The Dependency Rule

The dependency rule says: **dependencies always point inward**. Your core business logic should never import or know about external infrastructure (databases, APIs, frameworks). Instead, the outer layers depend on the inner layers.

```
┌──────────────────────────────────────┐
│          Adapters (outer)            │
│  PostgresUserRepository              │
│  knows about psycopg2                │
│  implements UserRepository           │
│         │                            │
│         │ depends on                 │
│         ▼                            │
│ ┌──────────────────────────────┐     │
│ │     Ports + Domain (inner)   │     │
│ │  UserRepository (interface)  │     │
│ │  UserService (business logic)│     │
│ │  knows about NOTHING external│     │
│ └──────────────────────────────┘     │
└──────────────────────────────────────┘
```

### Dependency Rule — With Port and Adapter ✅

```python
# domain.py — inner layer (ZERO external imports)
from abc import ABC, abstractmethod


class UserRepository(ABC):
    @abstractmethod
    def get_user(self, user_id: int) -> dict:
        ...


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def greet(self, user_id: int) -> str:
        user = self.repo.get_user(user_id)
        return f"Hello, {user['name']}!"
```

```python
# adapters.py — outer layer (imports domain + external libs)
import psycopg2
from domain import UserRepository


class PostgresUserRepository(UserRepository):
    def __init__(self, connection_string: str):
        self.connection_string = connection_string

    def get_user(self, user_id: int) -> dict:
        conn = psycopg2.connect(self.connection_string)
        cur = conn.cursor()
        cur.execute("SELECT name FROM users WHERE id = %s", (user_id,))
        name = cur.fetchone()[0]
        cur.close()
        conn.close()
        return {"id": user_id, "name": name}
```

```python
# main.py — wires it together
from domain import UserService
from adapters import PostgresUserRepository

repo = PostgresUserRepository("dbname=mydb user=admin password=secret")
service = UserService(repo)
print(service.greet(1))
```

**Notice:** `domain.py` has zero knowledge of `psycopg2`. If you delete Postgres tomorrow and switch to MongoDB, `domain.py` doesn't change at all — you just write a new adapter.

### Dependency Rule — Violated ❌

```python
# everything in one file — domain depends directly on psycopg2
import psycopg2


class UserService:
    def greet(self, user_id: int) -> str:
        conn = psycopg2.connect("dbname=mydb user=admin password=secret")
        cur = conn.cursor()
        cur.execute("SELECT name FROM users WHERE id = %s", (user_id,))
        name = cur.fetchone()[0]
        cur.close()
        conn.close()
        return f"Hello, {name}!"
```

**The problem:** `UserService` (business logic) directly imports and calls `psycopg2` (infrastructure). The dependency arrow points **outward**. If you switch databases, you rewrite your business logic. If `psycopg2` changes its API, your business logic breaks.
