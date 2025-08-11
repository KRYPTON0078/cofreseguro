"""URL scorer tests."""

from cofreseguro.analyze.url_score import score_url, score_urls_in_text


def test_shortener() -> None:
    result = score_url("https://bit.ly/abc123")
    assert result.score >= 0.3
    assert "url_shortener" in result.reasons


def test_extract() -> None:
    scores = score_urls_in_text("Click https://example.com/login now")
    assert len(scores) == 1
