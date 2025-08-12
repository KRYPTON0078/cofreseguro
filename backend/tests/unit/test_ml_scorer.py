"""ML scorer tests."""

from cofreseguro.analyze.ml_scorer import score_text


def test_score_range() -> None:
    result = score_text("URGENT!!! click http://evil.test send PIN 1234")
    assert 0.0 <= result.score <= 1.0
