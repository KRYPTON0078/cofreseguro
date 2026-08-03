from cofreseguro.literacy.tips import tip_for

def test_tip_invoice_en():
    t = tip_for(["invoice"], "en")
    assert isinstance(t, str) and len(t) > 10

def test_tip_invoice_pt():
    t = tip_for(["invoice"], "pt")
    assert isinstance(t, str) and len(t) > 10
