from app.pipeline import run
from data.memory import InMemoryStore
from model.transform import Payload


def test_run_pipeline() -> None:
    store = InMemoryStore()
    store.write(Payload(text="  hello  "))
    result = run(store, store)
    assert result == Payload(text="hello", count=5)
