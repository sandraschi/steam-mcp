from __future__ import annotations

from ..client import get_client
from ..config import settings
from ..formatters import error, games_md, result

BASE = "https://api.steampowered.com"
STORE_BASE = "https://store.steampowered.com"


def _require_key() -> dict | None:
    if not settings.has_api_key:
        return error("STEAM_API_KEY not configured")
    return None


async def get_owned_games(steamid: str = "", include_free: bool = False) -> dict:
    if err := _require_key():
        return err
    sid = steamid or settings.steam_id
    if not sid:
        return error("No steamid provided and STEAM_ID not configured")
    client = get_client()
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
        return error(f"API error: {resp.status_code}")
    response = resp.json().get("response", {})
    games = response.get("games", [])
    count = response.get("game_count", len(games))
    md = games_md(games, f"Owned games ({count})")
    return result(True, md, {"game_count": count, "games": games})


async def get_recently_played_games(steamid: str = "", count: int = 10) -> dict:
    if err := _require_key():
        return err
    sid = steamid or settings.steam_id
    if not sid:
        return error("No steamid provided and STEAM_ID not configured")
    client = get_client()
    resp = await client.get(
        f"{BASE}/IPlayerService/GetRecentlyPlayedGames/v1/",
        params={"key": settings.steam_api_key, "steamid": sid, "count": count},
    )
    if resp.status_code != 200:
        return error(f"API error: {resp.status_code}")
    games = resp.json().get("response", {}).get("games", [])
    md = games_md(games, f"Recently played ({len(games)})")
    return result(True, md, {"games": games})


async def get_app_details(app_id: int, country: str = "US") -> dict:
    client = get_client()
    resp = await client.get(
        f"{STORE_BASE}/api/appdetails",
        params={"appids": app_id, "cc": country, "l": "en"},
    )
    if resp.status_code != 200:
        return error(f"Store API error: {resp.status_code}")
    app_data = resp.json().get(str(app_id))
    if not app_data or not app_data.get("success"):
        return error("App not found or API returned no data")
    data = app_data.get("data", {})
    name = data.get("name", str(app_id))
    price = data.get("price_overview", {}).get("final_formatted", "Free" if data.get("is_free") else "N/A")
    md = f"## {name}\n\n- **App ID:** `{app_id}`\n- **Price:** {price}\n- **Free:** {data.get('is_free')}"
    return result(True, md, data)


async def get_wishlist(steamid: str = "") -> dict:
    if err := _require_key():
        return err
    sid = steamid or settings.steam_id
    if not sid:
        return error("No steamid provided and STEAM_ID not configured")
    client = get_client()
    resp = await client.get(
        f"{BASE}/IWishlistService/GetWishlist/v1/",
        params={"key": settings.steam_api_key, "steamid": sid},
    )
    if resp.status_code != 200:
        return error(f"API error: {resp.status_code}")
    items = resp.json().get("response", {}).get("items", [])
    lines = [f"## Wishlist ({len(items)} items)", ""]
    for item in items[:25]:
        lines.append(f"- App `{item.get('appid')}` — priority {item.get('priority', 0)}")
    return result(True, "\n".join(lines), {"items": items})
