from cofreseguro.literacy.tips import tip_for

def test_tip_qr_hijack_en():
    t = tip_for(["qr_hijack"], "en")
    assert isinstance(t, str) and len(t) > 10

def test_tip_qr_hijack_pt():
    t = tip_for(["qr_hijack"], "pt")
    assert isinstance(t, str) and len(t) > 10
