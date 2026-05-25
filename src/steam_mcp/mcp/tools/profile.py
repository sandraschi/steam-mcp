from typing import Annotated

from pydantic import Field

from ...config import settings
from ..registry import mcp

BASE = "https://api.steampowered.com"


def _headers():
    return {"key": settings.steam_api_key} if settings.has_api_key else {}


@mcp.tool(version="0.1.0")
async def get_own_profile() -> dict:
    """Get the player summary for the configured Steam account.

    Requires STEAM_API_KEY and STEAM_ID to be set.

    ## Return Format
    {"success": bool, "message": str, "data": {"player": {...}} | None}
    """
    if not settings.has_api_key:
        return {"success": False, "message": "STEAM_API_KEY not configured", "data": None}
    if not settings.has_steam_id:
        return {"success": False, "message": "STEAM_ID not configured", "data": None}

    import httpx

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{BASE}/ISteamUser/GetPlayerSummaries/v2/",
            params={"key": settings.steam_api_key, "steamids": settings.steam_id},
        )
        if resp.status_code != 200:
            return {"success": False, "message": f"API error: {resp.status_code}", "data": None}
        data = resp.json()
        players = data.get("response", {}).get("players", [])
        if not players:
            return {"success": False, "message": "Player not found", "data": None}
        return {"success": True, "message": "Profile retrieved", "data": {"player": players[0]}}


@mcp.tool(version="0.1.0")
async def get_player_summaries(
    steamids: Annotated[str, Field(description="Comma-separated 64-bit Steam IDs.")],
) -> dict:
    """Get player summaries for one or more Steam IDs.

    Requires STEAM_API_KEY.

    ## Return Format
    {"success": bool, "message": str, "data": {"players": [...]}}
    """
    if not settings.has_api_key:
        return {"success": False, "message": "STEAM_API_KEY not configured", "data": None}

    import httpx

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{BASE}/ISteamUser/GetPlayerSummaries/v2/",
            params={"key": settings.steam_api_key, "steamids": steamids},
        )
        if resp.status_code != 200:
            return {"success": False, "message": f"API error: {resp.status_code}", "data": None}
        data = resp.json()
        players = data.get("response", {}).get("players", [])
        return {"success": True, "message": f"Found {len(players)} players", "data": {"players": players}}


@mcp.tool(version="0.1.0")
async def get_friend_list(
    steamid: Annotated[str, Field(description="64-bit Steam ID of the user.")],
    relationship: Annotated[str, Field(description="Relationship filter: 'all' or 'friend'.")] = "all",
) -> dict:
    """Get the friend list for a Steam user.

    Requires STEAM_API_KEY.

    ## Return Format
    {"success": bool, "message": str, "data": {"friends": [...]}}
    """
    if not settings.has_api_key:
        return {"success": False, "message": "STEAM_API_KEY not configured", "data": None}

    import httpx

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{BASE}/ISteamUser/GetFriendList/v1/",
            params={"key": settings.steam_api_key, "steamid": steamid, "relationship": relationship},
        )
        if resp.status_code != 200:
            return {"success": False, "message": f"API error: {resp.status_code}", "data": None}
        data = resp.json()
        friends = data.get("friendslist", {}).get("friends", [])
        return {"success": True, "message": f"Found {len(friends)} friends", "data": {"friends": friends}}


@mcp.tool(version="0.1.0")
async def resolve_vanity_url(
    vanity_url: Annotated[str, Field(description="Custom URL portion. e.g. 'sandra' from steamcommunity.com/id/sandra")],
) -> dict:
    """Resolve a Steam custom vanity URL to a 64-bit Steam ID.

    Requires STEAM_API_KEY.

    ## Return Format
    {"success": bool, "message": str, "data": {"steamid": str} | None}
    """
    if not settings.has_api_key:
        return {"success": False, "message": "STEAM_API_KEY not configured", "data": None}

    import httpx

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{BASE}/ISteamUser/ResolveVanityURL/v1/",
            params={"key": settings.steam_api_key, "vanityurl": vanity_url},
        )
        if resp.status_code != 200:
            return {"success": False, "message": f"API error: {resp.status_code}", "data": None}
        data = resp.json()
        response = data.get("response", {})
        if response.get("success") != 1:
            return {"success": False, "message": response.get("message", "Vanity URL not found"), "data": None}
        return {"success": True, "message": "Steam ID resolved", "data": {"steamid": response["steamid"]}}
