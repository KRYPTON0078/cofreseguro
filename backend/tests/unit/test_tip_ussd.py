from cofreseguro.literacy.tips import tip_for

def test_tip_ussd_en():
    t = tip_for(["ussd"], "en")
    assert isinstance(t, str) and len(t) > 10

def test_tip_ussd_pt():
    t = tip_for(["ussd"], "pt")
    assert isinstance(t, str) and len(t) > 10
