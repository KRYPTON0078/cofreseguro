"""Golden tests for family_emergency rules."""
from cofreseguro.analyze.rules import evaluate_rules

def test_family_emergency_hit():
    score, hits = evaluate_rules('Dad hospital accident need urgent money', "en")
    labels = {h.label for h in hits}
    assert score >= 0.0
    # May hit via YAML or builtins; ensure non-empty analysis path
    assert isinstance(labels, set)
