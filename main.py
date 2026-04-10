# Composition Root (aka "main" or "bootstrap").
#
# This is the ONLY place in the entire project that knows about concrete
# adapters. It wires an adapter (SqliteStore) to the application layer's
# use case (write_user_input) through the port (PayloadWriter protocol).
#
# In Ports & Adapters, the composition root sits OUTSIDE the hexagon.
# It is not part of domain, application, or adapter layers — it just
# assembles them together.
from application.services import write_user_input
from adapters.sqlite_store import SqliteStore


def main() -> None:
    store = SqliteStore("data/data.db")
    user_text = input("Enter text: ")
    result = write_user_input(store, user_text)
    print(f"Saved: {result}")


if __name__ == "__main__":
    main()
