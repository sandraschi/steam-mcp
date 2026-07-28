from __future__ import annotations

from ..client import get_client
from ..formatters import error, result, store_search_md

BASE = "https://api.steampowered.com"
STORE_BASE = "https://store.steampowered.com"


async def get_news_for_app(app_id: int, count: int = 5, max_length: int = 0) -> dict:
    client = get_client()
    params: dict = {"appid": app_id, "count": count}
    if max_length:
        params["maxlength"] = max_length
    resp = await client.get(f"{BASE}/ISteamNews/GetNewsForApp/v2/", params=params)
    if resp.status_code != 200:
        return error(f"API error: {resp.status_code}")
    items = resp.json().get("appnews", {}).get("newsitems", [])
    lines = [f"## News — app `{app_id}`", ""]
    for item in items[:count]:
        lines.append(f"- **{item.get('title', '?')}** ({item.get('date', '?')})")
    return result(True, "\n".join(lines), {"appid": app_id, "newsitems": items})


async def search_store(query: str, count: int = 10) -> dict:
    client = get_client()
    resp = await client.get(f"https://steamcommunity.com/actions/SearchApps/{query}")
    if resp.status_code != 200:
        return error(f"Search API error: {resp.status_code}")
    results = resp.json()[:count]
    md = store_search_md(query, results)
    return result(True, md, {"query": query, "results": results})


async def get_app_reviews(app_id: int, count: int = 10) -> dict:
    client = get_client()
    resp = await client.get(
        f"{STORE_BASE}/appreviews/{app_id}",
        params={"json": 1, "num_per_page": count, "language": "english"},
    )
    if resp.status_code != 200:
        return error(f"Reviews API error: {resp.status_code}")
    data = resp.json()
    summary = data.get("query_summary", {})
    reviews = data.get("reviews", [])
    lines = [
        f"## Reviews — app `{app_id}`",
        f"- **Total:** {summary.get('total_reviews', 0)}",
        f"- **Score:** {summary.get('review_score_desc', 'N/A')}",
        "",
    ]
    for r in reviews[:count]:
        lines.append(f"- **{r.get('author', {}).get('steamid', '?')}**: {r.get('review', '')[:120]}…")
    return result(True, "\n".join(lines), {"summary": summary, "reviews": reviews})
