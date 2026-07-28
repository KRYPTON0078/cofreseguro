"""Auth hardening integration."""
import pytest

@pytest.mark.asyncio
async def test_login_returns_refresh(client):
    login = await client.post("/v1/auth/login", json={"email":"demo@cofreseguro.app","password":"demo123!"})
    assert login.status_code == 200
    body = login.json()
    assert "access_token" in body
    assert body.get("refresh_token")

@pytest.mark.asyncio
async def test_weak_register_rejected(client):
    resp = await client.post("/v1/auth/register", json={"email":"weak@example.com","password":"short"})
    assert resp.status_code in {400, 422}
