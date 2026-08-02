"""Behaviour endpoint tests."""
import pytest

@pytest.mark.asyncio
async def test_behaviour_me(client):
    login = await client.post("/v1/auth/login", json={"email":"demo@cofreseguro.app","password":"demo123!"})
    token = login.json()["access_token"]
    resp = await client.get("/v1/behaviour/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert "risk_score" in resp.json()
