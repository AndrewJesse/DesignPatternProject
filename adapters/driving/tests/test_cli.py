# Tests for the driving CLI adapter.
#
# Verifies that the CLI adapter correctly reads user input, passes it
# through the use case, and prints the result — without real I/O.
import unittest
from unittest.mock import patch
from io import StringIO

from adapters.driven.in_memory_store import InMemoryStore
from adapters.driving.cli import run


class TestCliAdapter(unittest.TestCase):
    @patch("builtins.input", return_value="  hello world  ")
    @patch("sys.stdout", new_callable=StringIO)
    def test_run_writes_input_and_prints_result(self, mock_stdout, mock_input):
        store = InMemoryStore()
        run(store)
        # The use case trims whitespace, so stored text should be trimmed
        self.assertEqual(store.last().text, "hello world")
        # Output should contain "Saved:"
        self.assertIn("Saved:", mock_stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
