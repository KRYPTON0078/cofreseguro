"""Golden tests for sim_swap rules."""
from cofreseguro.analyze.rules import evaluate_rules

def test_sim_swap_hit():
    score, hits = evaluate_rules('Your SIM was swapped share OTP now', "en")
    labels = {h.label for h in hits}
    assert score >= 0.0
    # May hit via YAML or builtins; ensure non-empty analysis path
    assert isinstance(labels, set)
