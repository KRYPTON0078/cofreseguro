"""Shared fixtures."""

import pytest
from httpx import ASGITransport, AsyncClient

from cofreseguro.main import create_app, seed_demo_users
from cofreseguro.shared.config import get_settings
from cofreseguro.shared.database import init_db, reset_engine


@pytest.fixture
async def client(tmp_path, monkeypatch):
    db = tmp_path / "test.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite+aiosqlite:///{db}")
    monkeypatch.setenv("OLLAMA_ENABLED", "false")
    get_settings.cache_clear()
    reset_engine()
    app = create_app()
    await init_db()
    await seed_demo_users()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    get_settings.cache_clear()
    reset_engine()
