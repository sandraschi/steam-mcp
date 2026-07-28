from __future__ import annotations

from ..client import get_client
from ..config import settings
from ..formatters import error, players_md, result

BASE = "https://api.steampowered.com"


def _require_key() -> dict | None:
    if not settings.has_api_key:
        return error("STEAM_API_KEY not configured")
    return None


async def get_own_profile() -> dict:
    if err := _require_key():
        return err
    if not settings.has_steam_id:
        return error("STEAM_ID not configured")
    return await get_player_summaries(settings.steam_id)


async def get_player_summaries(steamids: str) -> dict:
    if err := _require_key():
        return err
    client = get_client()
    resp = await client.get(
        f"{BASE}/ISteamUser/GetPlayerSummaries/v2/",
        params={"key": settings.steam_api_key, "steamids": steamids},
    )
    if resp.status_code != 200:
        return error(f"API error: {resp.status_code}")
    players = resp.json().get("response", {}).get("players", [])
    if not players:
        return error("Player not found")
    md = players_md(players)
    return result(True, md, {"players": players})


async def get_friend_list(steamid: str, relationship: str = "all") -> dict:
    if err := _require_key():
        return err
    client = get_client()
    resp = await client.get(
        f"{BASE}/ISteamUser/GetFriendList/v1/",
        params={"key": settings.steam_api_key, "steamid": steamid, "relationship": relationship},
    )
    if resp.status_code != 200:
        return error(f"API error: {resp.status_code}")
    friends = resp.json().get("friendslist", {}).get("friends", [])
    lines = [f"## Friends ({len(friends)})", ""]
    for f in friends[:30]:
        lines.append(f"- `{f.get('steamid')}` — since {f.get('friend_since', '?')}")
    return result(True, "\n".join(lines), {"friends": friends})


async def resolve_vanity_url(vanity_url: str) -> dict:
    if err := _require_key():
        return err
    client = get_client()
    resp = await client.get(
        f"{BASE}/ISteamUser/ResolveVanityURL/v1/",
        params={"key": settings.steam_api_key, "vanityurl": vanity_url},
    )
    if resp.status_code != 200:
        return error(f"API error: {resp.status_code}")
    response = resp.json().get("response", {})
    if response.get("success") != 1:
        return error(response.get("message", "Vanity URL not found"))
    sid = response["steamid"]
    return result(True, f"Resolved `{vanity_url}` → `{sid}`", {"steamid": sid})
