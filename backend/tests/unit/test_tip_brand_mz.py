from cofreseguro.literacy.tips import tip_for

def test_tip_brand_mz_en():
    t = tip_for(["brand_mz"], "en")
    assert isinstance(t, str) and len(t) > 10

def test_tip_brand_mz_pt():
    t = tip_for(["brand_mz"], "pt")
    assert isinstance(t, str) and len(t) > 10
