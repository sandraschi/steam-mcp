from typing import Annotated

from pydantic import Field

from ..registry import mcp

BASE = "https://api.steampowered.com"
STORE_BASE = "https://store.steampowered.com"


@mcp.tool(version="0.1.0")
async def get_news_for_app(
    app_id: Annotated[int, Field(description="Steam App ID (e.g. 440).")],
    count: Annotated[int, Field(description="Number of news items to return.", ge=1, le=100)] = 5,
    max_length: Annotated[int, Field(description="Max characters per news item.", ge=0)] = 0,
) -> dict:
    """Get the latest news for a Steam app.

    No API key required.

    ## Return Format
    {"success": bool, "message": str, "data": {"appid": int, "newsitems": [...]}}
    """
    import httpx

    params = {"appid": app_id, "count": count, "maxlength": max_length} if max_length else {"appid": app_id, "count": count}
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{BASE}/ISteamNews/GetNewsForApp/v2/", params=params)
        if resp.status_code != 200:
            return {"success": False, "message": f"API error: {resp.status_code}", "data": None}
        data = resp.json()
        items = data.get("appnews", {}).get("newsitems", [])
        return {
            "success": True,
            "message": f"Found {len(items)} news items",
            "data": {"appid": app_id, "newsitems": items},
        }


@mcp.tool(version="0.1.1")
async def search_store(
    query: Annotated[str, Field(description="Search query.")],
    count: Annotated[int, Field(description="Max results.", ge=1, le=20)] = 10,
) -> dict:
    """Search the Steam store for apps by name.

    Uses the Steam community search API. No API key required.

    ## Return Format
    {"success": bool, "message": str, "data": {"query": str, "results": [{"appid": str, "name": str, "icon": str}]}}
    """
    import httpx

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"https://steamcommunity.com/actions/SearchApps/{query}",
            headers={"User-Agent": "steam-mcp/0.1.0"},
        )
        if resp.status_code != 200:
            return {"success": False, "message": f"Search API error: {resp.status_code}", "data": None}
        results = resp.json()[:count]
        return {
            "success": True,
            "message": f"Found {len(results)} results for '{query}'",
            "data": {"query": query, "results": results},
        }
