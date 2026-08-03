from cofreseguro.literacy.tips import tip_for

def test_tip_brand_ao_en():
    t = tip_for(["brand_ao"], "en")
    assert isinstance(t, str) and len(t) > 10

def test_tip_brand_ao_pt():
    t = tip_for(["brand_ao"], "pt")
    assert isinstance(t, str) and len(t) > 10
