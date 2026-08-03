from cofreseguro.literacy.tips import tip_for

def test_tip_crypto_en():
    t = tip_for(["crypto"], "en")
    assert isinstance(t, str) and len(t) > 10

def test_tip_crypto_pt():
    t = tip_for(["crypto"], "pt")
    assert isinstance(t, str) and len(t) > 10
