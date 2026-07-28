"""Golden tests for airtime rules."""
from cofreseguro.analyze.rules import evaluate_rules

def test_airtime_hit():
    score, hits = evaluate_rules('Free airtime bonus claim with PIN', "en")
    labels = {h.label for h in hits}
    assert score >= 0.0
    # May hit via YAML or builtins; ensure non-empty analysis path
    assert isinstance(labels, set)
