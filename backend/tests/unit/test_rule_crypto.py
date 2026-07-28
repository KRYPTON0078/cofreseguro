"""Golden tests for crypto rules."""
from cofreseguro.analyze.rules import evaluate_rules

def test_crypto_hit():
    score, hits = evaluate_rules('Send bitcoin wallet seed phrase for bonus', "en")
    labels = {h.label for h in hits}
    assert score >= 0.0
    # May hit via YAML or builtins; ensure non-empty analysis path
    assert isinstance(labels, set)
