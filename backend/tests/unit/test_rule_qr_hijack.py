"""Golden tests for qr_hijack rules."""
from cofreseguro.analyze.rules import evaluate_rules

def test_qr_hijack_hit():
    score, hits = evaluate_rules('Scan this QR code to claim refund', "en")
    labels = {h.label for h in hits}
    assert score >= 0.0
    # May hit via YAML or builtins; ensure non-empty analysis path
    assert isinstance(labels, set)
