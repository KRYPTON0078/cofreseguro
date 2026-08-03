from cofreseguro.behaviour.explain import explain_behaviour

def test_explain_en():
    assert "high-risk" in explain_behaviour(10, 3, "en")

def test_explain_pt():
    assert "alto risco" in explain_behaviour(10, 3, "pt")
