import unittest

from app.pipeline import run
from data.memory import InMemoryStore
from model.transform import Payload


class TestPipeline(unittest.TestCase):
    def test_run_pipeline(self) -> None:
        store = InMemoryStore()
        store.write(Payload(text="  hello  "))
        result = run(store, store)
        self.assertEqual(result, Payload(text="hello", count=5))


if __name__ == "__main__":
    unittest.main()
