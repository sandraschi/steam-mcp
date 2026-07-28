from __future__ import annotations

from ..client import get_client
from ..config import settings
from ..formatters import error, result

BASE = "https://api.steampowered.com"

SORT_MAP = {
    "mostrecent": 1,
    "score": 2,
    "trend": 4,
    "mostsubscribed": 8,
    "mostfavorited": 12,
    "mostunsubscribed": 16,
}


def _require_key() -> dict | None:
    if not settings.has_api_key:
        return error("STEAM_API_KEY not configured")
    return None


async def query_workshop_items(
    app_id: int,
    query: str = "",
    count: int = 20,
    sort_by: str = "mostsubscribed",
    return_tags: bool = False,
) -> dict:
    if err := _require_key():
        return err
    sort_order = SORT_MAP.get(sort_by, 8)
    body = {
        "appid": app_id,
        "query_type": 1,
        "numperpage": count,
        "cursor": "*",
        "order_method": sort_order,
        "search_text": query or "",
        "return_tags": return_tags,
    }
    client = get_client()
    resp = await client.post(
        f"{BASE}/IPublishedFileService/QueryFiles/v1/",
        params={"key": settings.steam_api_key},
        json=body,
    )
    if resp.status_code != 200:
        return error(f"API error: {resp.status_code}")
    response = resp.json().get("response", {})
    files = response.get("publishedfiledetails", [])
    total = response.get("total", 0)
    lines = [f"## Workshop — app `{app_id}` ({total} items)", ""]
    for f in files[:15]:
        lines.append(f"- **{f.get('title', '?')}** — id `{f.get('publishedfileid')}`")
    return result(True, "\n".join(lines), {"items": files, "total": total})


async def get_workshop_item_details(published_file_ids: str) -> dict:
    if err := _require_key():
        return err
    ids = [x.strip() for x in published_file_ids.split(",") if x.strip()]
    if not ids:
        return error("Provide at least one published_file_id")
    client = get_client()
    resp = await client.post(
        f"{BASE}/ISteamRemoteStorage/GetPublishedFileDetails/v1/",
        params={"key": settings.steam_api_key},
        data={"itemcount": len(ids), **{f"publishedfileids[{i}]": pid for i, pid in enumerate(ids)}},
    )
    if resp.status_code != 200:
        return error(f"API error: {resp.status_code}")
    details = resp.json().get("response", {}).get("publishedfiledetails", [])
    lines = ["## Workshop item details", ""]
    for d in details:
        lines.append(f"- **{d.get('title', '?')}** — {d.get('file_size', 0)} bytes")
    return result(True, "\n".join(lines), {"items": details})
