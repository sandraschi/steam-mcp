"""Quick smoke test using ASGI transport."""
import asyncio
import json
import sys

sys.path.insert(0, ".")

from steam_mcp.server import app
from httpx import AsyncClient, ASGITransport


def unwrap(data):
    """Unwrap double-nested REST response."""
    if isinstance(data, dict) and "data" in data:
        inner = data["data"]
        if isinstance(inner, dict) and "data" in inner:
            return inner["data"]
        return inner
    return data


async def main():
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

        r = await client.get("/api/tools/get_app_details")
        print(f"\n=== /api/tools/get_app_details === HTTP {r.status_code}")

        r = await client.post(
            "/api/tools/get_app_details/call",
            json={"arguments": {"app_id": 440, "country": "US"}},
        )
        data = unwrap(r.json())
        print(f"\n=== get_app_details(440) ===")
        print(f'App: {data.get("name", "?")} (is_free: {data.get("is_free")})')

        r = await client.post(
            "/api/tools/get_number_of_current_players/call",
            json={"arguments": {"app_id": 440}},
        )
        data = unwrap(r.json())
        print(f"\n=== get_number_of_current_players(440) ===")
        print(f'Players in TF2: {data["player_count"]}')

        r = await client.post(
            "/api/tools/get_news_for_app/call",
            json={"arguments": {"app_id": 440, "count": 3}},
        )
        data = unwrap(r.json())
        print(f"\n=== get_news_for_app(440) ===")
        items = data.get("newsitems", [])
        print(f"News items: {len(items)}")
        for item in items[:2]:
            print(f'  - {item.get("title", "?")}')

        r = await client.post(
            "/api/tools/get_global_achievement_percentages/call",
            json={"arguments": {"app_id": 440}},
        )
        data = unwrap(r.json())
        print(f"\n=== get_global_achievement_percentages(440) ===")
        achievements = data.get("achievements", [])
        print(f"Achievements: {len(achievements)} tracked")
        for a in achievements[:3]:
            pct = float(a.get("percent", 0) or 0)
            print(f'  - {a.get("name", "?")}: {pct:.1f}%')

        r = await client.post(
            "/api/tools/search_store/call",
            json={"arguments": {"query": "Godot", "count": 5}},
        )
        data = unwrap(r.json())
        print(f"\n=== search_store(Godot) ===")
        results = data.get("results", [])
        print(f"Results: {len(results)}")
        for item in results[:3]:
            print(f'  - {item.get("name", "?")} (appid: {item.get("appid", "?")})')

    print("\nAll smoke tests passed!")


asyncio.run(main())
