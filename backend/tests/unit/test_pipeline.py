"""Pipeline tests."""

import pytest

from cofreseguro.analyze.pipeline import analyze_text


@pytest.mark.asyncio
async def test_analyze_high_risk() -> None:
    result = await analyze_text(
        "URGENT: send your PIN and click https://bit.ly/mpesa-win",
        "en",
    )
    assert result.risk_level in {"medium", "high", "critical"}
    assert result.tip
