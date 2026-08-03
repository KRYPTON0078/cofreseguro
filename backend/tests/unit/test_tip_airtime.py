from cofreseguro.literacy.tips import tip_for

def test_tip_airtime_en():
    t = tip_for(["airtime"], "en")
    assert isinstance(t, str) and len(t) > 10

def test_tip_airtime_pt():
    t = tip_for(["airtime"], "pt")
    assert isinstance(t, str) and len(t) > 10
