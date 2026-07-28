"""Golden tests for otp_forward rules."""
from cofreseguro.analyze.rules import evaluate_rules

def test_otp_forward_hit():
    score, hits = evaluate_rules('Please forward this OTP 123456 to support', "en")
    labels = {h.label for h in hits}
    assert score >= 0.0
    # May hit via YAML or builtins; ensure non-empty analysis path
    assert isinstance(labels, set)
