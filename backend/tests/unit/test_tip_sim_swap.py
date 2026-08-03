from cofreseguro.literacy.tips import tip_for

def test_tip_sim_swap_en():
    t = tip_for(["sim_swap"], "en")
    assert isinstance(t, str) and len(t) > 10

def test_tip_sim_swap_pt():
    t = tip_for(["sim_swap"], "pt")
    assert isinstance(t, str) and len(t) > 10
