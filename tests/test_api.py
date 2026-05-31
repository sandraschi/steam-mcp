import sys
from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))


@pytest.fixture
async def client():
    from steam_mcp.client import close_client, init_client
    from steam_mcp.server import app

    await init_client()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    await close_client()


@pytest.mark.asyncio
async def test_health(client):
    r = await client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_api_status(client):
    r = await client.get("/api/status")
    data = r.json()
    assert data["status"] == "ok"
    assert data["version"] == "0.2.0"
    assert data["tool_count"] >= 10


@pytest.mark.asyncio
async def test_store_search_no_key(client):
    r = await client.post(
        "/api/tools/steam_store/call",
        json={"arguments": {"operation": "search", "query": "Godot", "count": 3}},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["success"] is True
    inner = body["data"]
    assert inner.get("success") is True


@pytest.mark.asyncio
async def test_player_count(client):
    r = await client.post(
        "/api/tools/steam_stats/call",
        json={"arguments": {"operation": "players", "app_id": 440}},
    )
    assert r.status_code == 200
    data = r.json()["data"]
    assert data["success"] is True
    assert data["data"]["player_count"] >= 0
