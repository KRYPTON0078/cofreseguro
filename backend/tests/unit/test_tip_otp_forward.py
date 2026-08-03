from cofreseguro.literacy.tips import tip_for

def test_tip_otp_forward_en():
    t = tip_for(["otp_forward"], "en")
    assert isinstance(t, str) and len(t) > 10

def test_tip_otp_forward_pt():
    t = tip_for(["otp_forward"], "pt")
    assert isinstance(t, str) and len(t) > 10
