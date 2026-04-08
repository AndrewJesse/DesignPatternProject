from model.transform import Payload, normalize


def test_normalize_strips_and_counts() -> None:
    out = normalize(Payload(text="  hello  "))
    assert out.text == "hello"
    assert out.count == 5


def test_normalize_empty() -> None:
    out = normalize(Payload(text="   "))
    assert out.text == ""
    assert out.count == 0
