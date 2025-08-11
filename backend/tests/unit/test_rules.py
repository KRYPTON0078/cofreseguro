"""Rule engine tests."""

from cofreseguro.analyze.rules import evaluate_rules


def test_pin_request_en() -> None:
    score, hits = evaluate_rules("Please send your PIN to confirm", "en")
    assert score > 0.3
    assert any(h.label == "credential_harvest" for h in hits)


def test_safe_message() -> None:
    score, _hits = evaluate_rules("Your balance is 100 MZN", "en")
    assert score < 0.4
