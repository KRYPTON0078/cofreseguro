"""Literacy tip tests."""

from cofreseguro.literacy.tips import tip_for


def test_tip_pt() -> None:
    tip = tip_for(["credential_harvest"], "pt")
    assert "PIN" in tip or "OTP" in tip


def test_default_en() -> None:
    tip = tip_for([], "en")
    assert len(tip) > 10
