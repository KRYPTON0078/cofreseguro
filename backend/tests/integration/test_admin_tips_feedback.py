"""Admin, tips, and feedback integration."""
import pytest

@pytest.mark.asyncio
async def test_tips_list(client):
    resp = await client.get("/v1/tips")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

@pytest.mark.asyncio
async def test_admin_requires_admin(client):
    login = await client.post("/v1/auth/login", json={"email":"demo@cofreseguro.app","password":"demo123!"})
    token = login.json()["access_token"]
    resp = await client.get("/v1/admin/users", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 403

@pytest.mark.asyncio
async def test_admin_ok_and_feedback(client):
    login = await client.post("/v1/auth/login", json={"email":"admin@cofreseguro.app","password":"admin123!"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    assert (await client.get("/v1/admin/users", headers=headers)).status_code == 200
    # analyze as demo for feedback ownership
    demo = await client.post("/v1/auth/login", json={"email":"demo@cofreseguro.app","password":"demo123!"})
    dtok = demo.json()["access_token"]
    dheaders = {"Authorization": f"Bearer {dtok}"}
    analyzed = await client.post("/v1/analyze", headers=dheaders, json={"text":"send PIN https://bit.ly/x","locale":"en"})
    aid = analyzed.json()["id"]
    fb = await client.post("/v1/feedback", headers=dheaders, json={"analysis_id": aid, "verdict": "correct", "note": "ok"})
    assert fb.status_code == 200
