"""Readiness probe test."""
import pytest

@pytest.mark.asyncio
async def test_ready(client):
    resp = await client.get("/ready")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ready"
