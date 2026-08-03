from cofreseguro.literacy.tips import tip_for

def test_tip_loan_en():
    t = tip_for(["loan"], "en")
    assert isinstance(t, str) and len(t) > 10

def test_tip_loan_pt():
    t = tip_for(["loan"], "pt")
    assert isinstance(t, str) and len(t) > 10
