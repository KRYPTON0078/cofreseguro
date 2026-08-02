"""Portuguese rule coverage."""
from cofreseguro.analyze.rules import evaluate_rules

def test_pt_pin_urgency():
    score, hits = evaluate_rules("URGENTE: envie o PIN agora https://bit.ly/x", "pt")
    assert score > 0.3
    labels = {h.label for h in hits}
    assert "credential_harvest" in labels or "urgency" in labels
