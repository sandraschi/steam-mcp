from typing import Annotated

from pydantic import Field

from ...config import settings
from ..registry import mcp

BASE = "https://api.steampowered.com"


@mcp.tool(version="0.1.0")
async def get_player_achievements(
    steamid: Annotated[str, Field(description="64-bit Steam ID.")],
    app_id: Annotated[int, Field(description="Steam App ID (e.g. 440).")],
) -> dict:
    """Get the achievement list for a player in a specific game.

    Requires STEAM_API_KEY.

    ## Return Format
    {"success": bool, "message": str, "data": {"game_name": str, "achievements": [...]}}
    """
    if not settings.has_api_key:
        return {"success": False, "message": "STEAM_API_KEY not configured", "data": None}

    import httpx

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{BASE}/ISteamUserStats/GetPlayerAchievements/v1/",
            params={"key": settings.steam_api_key, "steamid": steamid, "appid": app_id, "l": "en"},
        )
        if resp.status_code != 200:
            return {"success": False, "message": f"API error: {resp.status_code}", "data": None}
        data = resp.json()
        player_stats = data.get("playerstats", {})
        if player_stats.get("error"):
            return {"success": False, "message": player_stats["error"], "data": None}
        achievements = player_stats.get("achievements", [])
        return {
            "success": True,
            "message": f"Found {len(achievements)} achievements",
            "data": {
                "game_name": player_stats.get("gameName", ""),
                "achievements": achievements,
            },
        }


@mcp.tool(version="0.1.0")
async def get_global_achievement_percentages(
    app_id: Annotated[int, Field(description="Steam App ID (e.g. 440).")],
) -> dict:
    """Get global achievement completion percentages for a game.

    No API key required.

    ## Return Format
    {"success": bool, "message": str, "data": {"achievements": [{"name": str, "percent": float}]}}
    """
    import httpx

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{BASE}/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v2/",
            params={"gameid": app_id},
        )
        if resp.status_code != 200:
            return {"success": False, "message": f"API error: {resp.status_code}", "data": None}
        data = resp.json()
        achievements = data.get("achievementpercentages", {}).get("achievements", [])
        return {
            "success": True,
            "message": f"Found {len(achievements)} achievement percentages",
            "data": {"achievements": achievements},
        }


@mcp.tool(version="0.1.0")
async def get_number_of_current_players(
    app_id: Annotated[int, Field(description="Steam App ID (e.g. 440).")],
) -> dict:
    """Get the current number of players for a Steam game.

    No API key required.

    ## Return Format
    {"success": bool, "message": str, "data": {"player_count": int}}
    """
    import httpx

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{BASE}/ISteamUserStats/GetNumberOfCurrentPlayers/v1/",
            params={"appid": app_id},
        )
        if resp.status_code != 200:
            return {"success": False, "message": f"API error: {resp.status_code}", "data": None}
        data = resp.json()
        count = data.get("response", {}).get("player_count", 0)
        return {
            "success": True,
            "message": f"{count} players currently in-game",
            "data": {"player_count": count},
        }


@mcp.tool(version="0.1.0")
async def get_game_leaderboards(
    app_id: Annotated[int, Field(description="Steam App ID.")],
) -> dict:
    """Get the list of leaderboards for a Steam game.

    Requires STEAM_API_KEY.

    ## Return Format
    {"success": bool, "message": str, "data": {"leaderboards": [...]}}
    """
    if not settings.has_api_key:
        return {"success": False, "message": "STEAM_API_KEY not configured", "data": None}

    import httpx

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{BASE}/ISteamLeaderboards/GetLeaderboardsForGame/v2/",
            params={"key": settings.steam_api_key, "appid": app_id},
        )
        if resp.status_code != 200:
            return {"success": False, "message": f"API error: {resp.status_code}", "data": None}
        data = resp.json()
        lbs = data.get("response", {}).get("leaderboards", [])
        return {
            "success": True,
            "message": f"Found {len(lbs)} leaderboards",
            "data": {"leaderboards": lbs},
        }
