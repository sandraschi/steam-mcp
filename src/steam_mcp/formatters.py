"""Markdown formatters for Steam MCP tool returns."""

from __future__ import annotations

from typing import Any


def result(success: bool, message: str, data: Any = None) -> dict[str, Any]:
    return {"success": success, "message": message, "data": data}


def error(message: str) -> dict[str, Any]:
    return result(False, message, None)


def players_md(players: list[dict]) -> str:
    lines = ["## Players", ""]
    for p in players[:20]:
        name = p.get("personaname", "Unknown")
        sid = p.get("steamid", "?")
        state = p.get("personastate", 0)
        lines.append(f"- **{name}** (`{sid}`) — state {state}")
    if len(players) > 20:
        lines.append(f"\n*…and {len(players) - 20} more*")
    return "\n".join(lines)


def games_md(games: list[dict], title: str = "Games") -> str:
    lines = [f"## {title}", ""]
    for g in games[:25]:
        name = g.get("name") or f"App {g.get('appid', '?')}"
        mins = (g.get("playtime_forever") or 0) // 60
        lines.append(f"- **{name}** — {mins}h played (app `{g.get('appid')}`)")
    if len(games) > 25:
        lines.append(f"\n*…and {len(games) - 25} more*")
    lines.append("\n**Next steps:** use `steam_library(operation='details', app_id=…)` for store info.")
    return "\n".join(lines)


def store_search_md(query: str, results: list[dict]) -> str:
    lines = [f"## Store search: `{query}`", ""]
    for item in results[:15]:
        lines.append(f"- **{item.get('name', '?')}** — app `{item.get('appid', '?')}`")
    if not results:
        lines.append("_No results._")
    return "\n".join(lines)


def status_md(has_key: bool, has_id: bool, tool_count: int) -> str:
    return "\n".join(
        [
            "## Steam-MCP Status",
            f"- **API key:** {'configured' if has_key else 'missing'}",
            f"- **Steam ID:** {'configured' if has_id else 'not set'}",
            f"- **Registered tools:** {tool_count}",
            "",
            "**Next steps:** set `STEAM_API_KEY` and `STEAM_ID` for profile/library tools.",
        ]
    )
