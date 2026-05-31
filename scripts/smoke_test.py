"""Quick smoke test using ASGI transport."""

import asyncio
import json
import sys

sys.path.insert(0, "src")

from httpx import ASGITransport, AsyncClient

from steam_mcp.client import close_client, init_client
from steam_mcp.server import app


def unwrap(data):
    if isinstance(data, dict) and "data" in data:
        inner = data["data"]
        if isinstance(inner, dict) and "data" in inner:
            return inner["data"]
        return inner
    return data


async def main():
    await init_client()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/status")
        print("=== /api/status ===")
        print(r.json())

        r = await client.get("/api/tools")
        data = r.json()
        print(f'\n=== /api/tools ({len(data["tools"])} tools) ===')
        for t in data["tools"]:
            print(f"  - {t['name']}")

        r = await client.post(
            "/api/tools/steam_library/call",
            json={"arguments": {"operation": "details", "app_id": 440, "country": "US"}},
        )
        data = unwrap(r.json())
        print(f"\n=== steam_library details(440) ===")
        print(f"App: {data.get('name', '?')} (free: {data.get('is_free')})")

        r = await client.post(
            "/api/tools/steam_stats/call",
            json={"arguments": {"operation": "players", "app_id": 440}},
        )
        data = unwrap(r.json())
        print(f"\n=== steam_stats players(440) ===")
        print(f"Players: {data['player_count']}")

        r = await client.post(
            "/api/tools/steam_store/call",
            json={"arguments": {"operation": "news", "app_id": 440, "count": 3}},
        )
        data = unwrap(r.json())
        print(f"\n=== steam_store news(440) ===")
        print(f"News items: {len(data.get('newsitems', []))}")

        r = await client.post(
            "/api/tools/steam_store/call",
            json={"arguments": {"operation": "search", "query": "Godot", "count": 3}},
        )
        data = unwrap(r.json())
        print(f"\n=== steam_store search(Godot) ===")
        for item in data.get("results", [])[:3]:
            print(f"  - {item.get('name')} ({item.get('appid')})")

    await close_client()
    print("\nAll smoke tests passed!")


asyncio.run(main())
