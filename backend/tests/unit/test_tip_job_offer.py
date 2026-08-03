from cofreseguro.literacy.tips import tip_for

def test_tip_job_offer_en():
    t = tip_for(["job_offer"], "en")
    assert isinstance(t, str) and len(t) > 10

def test_tip_job_offer_pt():
    t = tip_for(["job_offer"], "pt")
    assert isinstance(t, str) and len(t) > 10
