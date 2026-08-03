from cofreseguro.literacy.tips import tip_for

def test_tip_romance_en():
    t = tip_for(["romance"], "en")
    assert isinstance(t, str) and len(t) > 10

def test_tip_romance_pt():
    t = tip_for(["romance"], "pt")
    assert isinstance(t, str) and len(t) > 10
