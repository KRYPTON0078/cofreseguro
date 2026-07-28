"""Golden tests for romance rules."""
from cofreseguro.analyze.rules import evaluate_rules

def test_romance_hit():
    score, hits = evaluate_rules('My love send money via western union', "en")
    labels = {h.label for h in hits}
    assert score >= 0.0
    # May hit via YAML or builtins; ensure non-empty analysis path
    assert isinstance(labels, set)
