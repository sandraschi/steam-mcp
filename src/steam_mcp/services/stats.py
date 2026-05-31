from __future__ import annotations

from ..client import get_client
from ..config import settings
from ..formatters import error, result

BASE = "https://api.steampowered.com"


def _require_key() -> dict | None:
    if not settings.has_api_key:
        return error("STEAM_API_KEY not configured")
    return None


async def get_player_achievements(steamid: str, app_id: int) -> dict:
    if err := _require_key():
        return err
    client = get_client()
    resp = await client.get(
        f"{BASE}/ISteamUserStats/GetPlayerAchievements/v1/",
        params={"key": settings.steam_api_key, "steamid": steamid, "appid": app_id, "l": "en"},
    )
    if resp.status_code != 200:
        return error(f"API error: {resp.status_code}")
    player_stats = resp.json().get("playerstats", {})
    if player_stats.get("error"):
        return error(player_stats["error"])
    achievements = player_stats.get("achievements", [])
    unlocked = sum(1 for a in achievements if a.get("achieved"))
    game_name = player_stats.get("gameName", str(app_id))
    lines = [f"## Achievements — {game_name}", f"Unlocked **{unlocked}/{len(achievements)}**", ""]
    for a in achievements[:20]:
        mark = "✓" if a.get("achieved") else "○"
        lines.append(f"- {mark} {a.get('name', '?')}")
    return result(
        True,
        "\n".join(lines),
        {"game_name": game_name, "achievements": achievements},
    )


async def get_global_achievement_percentages(app_id: int) -> dict:
    client = get_client()
    resp = await client.get(
        f"{BASE}/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v2/",
        params={"gameid": app_id},
    )
    if resp.status_code != 200:
        return error(f"API error: {resp.status_code}")
    achievements = resp.json().get("achievementpercentages", {}).get("achievements", [])
    lines = [f"## Global achievements — app `{app_id}`", ""]
    for a in achievements[:15]:
        pct = float(a.get("percent", 0) or 0)
        lines.append(f"- {a.get('name', '?')}: **{pct:.1f}%**")
    return result(True, "\n".join(lines), {"achievements": achievements})


async def get_number_of_current_players(app_id: int) -> dict:
    client = get_client()
    resp = await client.get(
        f"{BASE}/ISteamUserStats/GetNumberOfCurrentPlayers/v1/",
        params={"appid": app_id},
    )
    if resp.status_code != 200:
        return error(f"API error: {resp.status_code}")
    count = resp.json().get("response", {}).get("player_count", 0)
    md = f"## Current players\n\n**{count:,}** players in app `{app_id}` right now."
    return result(True, md, {"player_count": count, "app_id": app_id})


async def get_game_leaderboards(app_id: int) -> dict:
    if err := _require_key():
        return err
    client = get_client()
    resp = await client.get(
        f"{BASE}/ISteamLeaderboards/GetLeaderboardsForGame/v2/",
        params={"key": settings.steam_api_key, "appid": app_id},
    )
    if resp.status_code != 200:
        return error(f"API error: {resp.status_code}")
    lbs = resp.json().get("response", {}).get("leaderboards", [])
    lines = [f"## Leaderboards — app `{app_id}`", ""]
    for lb in lbs[:20]:
        lines.append(f"- **{lb.get('name', '?')}** (id `{lb.get('leaderboardid')}`)")
    return result(True, "\n".join(lines), {"leaderboards": lbs})
