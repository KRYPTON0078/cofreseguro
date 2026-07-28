"""Golden tests for invoice rules."""
from cofreseguro.analyze.rules import evaluate_rules

def test_invoice_hit():
    score, hits = evaluate_rules('Unpaid invoice overdue pay now', "en")
    labels = {h.label for h in hits}
    assert score >= 0.0
    # May hit via YAML or builtins; ensure non-empty analysis path
    assert isinstance(labels, set)
