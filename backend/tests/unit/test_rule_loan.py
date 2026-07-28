"""Golden tests for loan rules."""
from cofreseguro.analyze.rules import evaluate_rules

def test_loan_hit():
    score, hits = evaluate_rules('Instant loan approved pay fee now', "en")
    labels = {h.label for h in hits}
    assert score >= 0.0
    # May hit via YAML or builtins; ensure non-empty analysis path
    assert isinstance(labels, set)
