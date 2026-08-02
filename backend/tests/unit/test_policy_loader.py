"""Policy loader tests."""
from cofreseguro.analyze.policy_loader import clear_policy_cache, load_rule_policies, load_url_fragments

def test_loads_rules_and_urls():
    clear_policy_cache()
    rules = load_rule_policies()
    urls = load_url_fragments()
    assert isinstance(rules, list)
    assert isinstance(urls, list)
