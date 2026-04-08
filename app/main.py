from app.pipeline import run
from data.memory import InMemoryStore
from model.transform import Payload


def main() -> None:
    store = InMemoryStore()
    store.write(Payload(text="  hello  "))
    result = run(store, store)
    print(result)
