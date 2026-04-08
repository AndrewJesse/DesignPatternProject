import unittest

from model.transform import Payload, normalize


class TestNormalize(unittest.TestCase):
    def test_strips_and_counts(self) -> None:
        out = normalize(Payload(text="  hello  "))
        self.assertEqual(out.text, "hello")
        self.assertEqual(out.count, 5)

    def test_empty(self) -> None:
        out = normalize(Payload(text="   "))
        self.assertEqual(out.text, "")
        self.assertEqual(out.count, 0)


if __name__ == "__main__":
    unittest.main()
