"""API integration tests."""

import pytest


@pytest.mark.asyncio
async def test_health(client):
    resp = await client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_login_analyze_history(client):
    login = await client.post(
        "/v1/auth/login",
        json={"email": "demo@cofreseguro.app", "password": "demo123!"},
    )
    assert login.status_code == 200
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    analyzed = await client.post(
        "/v1/analyze",
        headers=headers,
        json={"text": "Send your PIN now https://bit.ly/x", "locale": "en"},
    )
    assert analyzed.status_code == 200
    assert "risk_level" in analyzed.json()
    hist = await client.get("/v1/history", headers=headers)
    assert hist.status_code == 200
    assert len(hist.json()) >= 1
