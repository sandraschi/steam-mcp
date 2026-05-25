from typing import Annotated

from pydantic import Field

from ...config import settings
from ..registry import mcp

BASE = "https://api.steampowered.com"
STORE_BASE = "https://store.steampowered.com"


@mcp.tool(version="0.1.0")
async def get_owned_games(
    steamid: Annotated[str, Field(description="64-bit Steam ID. Defaults to configured STEAM_ID.")] = "",
    include_free: Annotated[bool, Field(description="Include free games.")] = False,
) -> dict:
    """Get the list of owned games with playtime for a Steam user.

    Requires STEAM_API_KEY. Defaults to configured STEAM_ID.

    ## Return Format
    {"success": bool, "message": str, "data": {"game_count": int, "games": [...]}}
    """
    if not settings.has_api_key:
        return {"success": False, "message": "STEAM_API_KEY not configured", "data": None}
    sid = steamid or settings.steam_id
    if not sid:
        return {"success": False, "message": "No steamid provided and STEAM_ID not configured", "data": None}

    import httpx

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{BASE}/IPlayerService/GetOwnedGames/v1/",
            params={
                "key": settings.steam_api_key,
                "steamid": sid,
                "include_appinfo": 1,
                "include_played_free_games": 1 if include_free else 0,
            },
        )
        if resp.status_code != 200:
            return {"success": False, "message": f"API error: {resp.status_code}", "data": None}
        data = resp.json()
        response = data.get("response", {})
        games = response.get("games", [])
        return {
            "success": True,
            "message": f"Found {response.get('game_count', len(games))} games",
            "data": {"game_count": response.get("game_count", len(games)), "games": games},
        }


@mcp.tool(version="0.1.0")
async def get_recently_played_games(
    steamid: Annotated[str, Field(description="64-bit Steam ID. Defaults to configured STEAM_ID.")] = "",
    count: Annotated[int, Field(description="Max games to return.", ge=1, le=50)] = 10,
) -> dict:
    """Get recently played games for a Steam user.

    Requires STEAM_API_KEY.

    ## Return Format
    {"success": bool, "message": str, "data": {"games": [...]}}
    """
    if not settings.has_api_key:
        return {"success": False, "message": "STEAM_API_KEY not configured", "data": None}
    sid = steamid or settings.steam_id
    if not sid:
        return {"success": False, "message": "No steamid provided and STEAM_ID not configured", "data": None}

    import httpx

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{BASE}/IPlayerService/GetRecentlyPlayedGames/v1/",
            params={"key": settings.steam_api_key, "steamid": sid, "count": count},
        )
        if resp.status_code != 200:
            return {"success": False, "message": f"API error: {resp.status_code}", "data": None}
        data = resp.json()
        games = data.get("response", {}).get("games", [])
        return {"success": True, "message": f"Found {len(games)} recently played games", "data": {"games": games}}


@mcp.tool(version="0.1.0")
async def get_app_details(
    app_id: Annotated[int, Field(description="Steam App ID (e.g. 440 for Team Fortress 2).")],
    country: Annotated[str, Field(description="ISO 3166-1 alpha-2 country code for price info.")] = "US",
) -> dict:
    """Get detailed store info for a Steam app. Uses the public Steam store API — no API key required.

    ## Return Format
    {"success": bool, "message": str, "data": {app details dict} | None}
    """
    import httpx

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{STORE_BASE}/api/appdetails",
            params={"appids": app_id, "cc": country, "l": "en"},
        )
        if resp.status_code != 200:
            return {"success": False, "message": f"Store API error: {resp.status_code}", "data": None}
        data = resp.json()
        app_data = data.get(str(app_id))
        if not app_data or not app_data.get("success"):
            return {"success": False, "message": "App not found or API returned no data", "data": None}
        return {"success": True, "message": "App details retrieved", "data": app_data.get("data", {})}
