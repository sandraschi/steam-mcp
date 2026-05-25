from typing import Annotated

from pydantic import Field

from ...config import settings
from ..registry import mcp

BASE = "https://api.steampowered.com"


@mcp.tool(version="0.1.0")
async def query_workshop_items(
    app_id: Annotated[int, Field(description="Steam App ID to query workshop for.")],
    query: Annotated[str, Field(description="Search text for workshop items.")] = "",
    count: Annotated[int, Field(description="Max items to return.", ge=1, le=100)] = 20,
    sort_by: Annotated[str, Field(description="Sort order. Options: 'score', 'trend', 'mostrecent', 'mostsubscribed', 'mostfavorited', 'mostunsubscribed'.")] = "mostsubscribed",
    return_tags: Annotated[bool, Field(description="Include item tags in results.")] = False,
) -> dict:
    """Query Steam Workshop items for a game.

    Requires STEAM_API_KEY.

    ## Return Format
    {"success": bool, "message": str, "data": {"items": [...], "total": int}}
    """
    if not settings.has_api_key:
        return {"success": False, "message": "STEAM_API_KEY not configured", "data": None}

    import httpx

    sort_map = {
        "mostrecent": 1,
        "score": 2,
        "trend": 4,
        "mostsubscribed": 8,
        "mostfavorited": 12,
        "mostunsubscribed": 16,
    }
    sort_order = sort_map.get(sort_by, 8)

    body = {
        "appid": app_id,
        "query_type": 1,
        "numperpage": count,
        "cursor": "*",
        "order_method": sort_order,
        "search_text": query or "",
        "return_tags": return_tags,
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{BASE}/IPublishedFileService/QueryFiles/v1/",
            params={"key": settings.steam_api_key},
            json=body,
        )
        if resp.status_code != 200:
            return {"success": False, "message": f"API error: {resp.status_code}", "data": None}
        data = resp.json()
        response = data.get("response", {})
        files = response.get("publishedfiledetails", [])
        total = response.get("total", 0)
        return {
            "success": True,
            "message": f"Found {total} workshop items",
            "data": {"items": files, "total": total},
        }
