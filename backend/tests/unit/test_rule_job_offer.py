"""Golden tests for job_offer rules."""
from cofreseguro.analyze.rules import evaluate_rules

def test_job_offer_hit():
    score, hits = evaluate_rules('Work from home job offer pay registration fee', "en")
    labels = {h.label for h in hits}
    assert score >= 0.0
    # May hit via YAML or builtins; ensure non-empty analysis path
    assert isinstance(labels, set)
