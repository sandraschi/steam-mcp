"""Lightweight chat orchestrator for the webapp — routes natural language to portmanteau tools."""

from __future__ import annotations

import re
from typing import Any

from .mcp.registry import mcp

_APP_ID = re.compile(r"\b(?:app\s*)?(?:id\s*)?(\d{3,8})\b", re.I)
_QUOTED = re.compile(r'"([^"]+)"|\'([^\']+)\'')


async def _call(tool: str, arguments: dict[str, Any]) -> str:
    result = await mcp.call_tool(tool, arguments)
    content = result.content[0].text if result.content else str(result)
    try:
        import json

        parsed = json.loads(content)
        if isinstance(parsed, dict):
            return str(parsed.get("message") or parsed)
    except (json.JSONDecodeError, TypeError, AttributeError):
        pass
    return content


def _extract_query(text: str) -> str | None:
    for match in _QUOTED.finditer(text):
        value = match.group(1) or match.group(2)
        if value:
            return value.strip()
    lowered = text.lower()
    for prefix in ("search for ", "find ", "look up ", "query "):
        if prefix in lowered:
            return text[lowered.index(prefix) + len(prefix) :].strip(" .")
    return None


def _extract_app_id(text: str, default: int = 440) -> int:
    match = _APP_ID.search(text)
    if match:
        return int(match.group(1))
    return default


async def handle_chat_query(query: str) -> dict[str, str]:
    """Map a user message to one or more portmanteau tool calls."""
    q = (query or "").strip()
    if not q:
        return {
            "response": (
                "Ask about Steam games, e.g.:\n"
                '- "search for Godot"\n'
                '- "how many players in app 440"\n'
                '- "show my library"\n'
                '- "news for 570"'
            )
        }

    lowered = q.lower()
    app_id = _extract_app_id(q)

    if any(k in lowered for k in ("my library", "owned games", "my games", "game library")):
        text = await _call("steam_library", {"operation": "owned"})
        return {"response": text, "tool": "steam_library", "operation": "owned"}

    if any(k in lowered for k in ("my profile", "own profile", "who am i")):
        text = await _call("steam_profile", {"operation": "own"})
        return {"response": text, "tool": "steam_profile", "operation": "own"}

    if "wishlist" in lowered:
        text = await _call("steam_library", {"operation": "wishlist"})
        return {"response": text, "tool": "steam_library", "operation": "wishlist"}

    if any(k in lowered for k in ("player count", "players online", "concurrent", "how many players", "players in")):
        text = await _call("steam_stats", {"operation": "players", "app_id": app_id})
        return {"response": text, "tool": "steam_stats", "operation": "players"}

    if "achievement" in lowered and "global" in lowered:
        text = await _call("steam_stats", {"operation": "global_percentages", "app_id": app_id})
        return {"response": text, "tool": "steam_stats", "operation": "global_percentages"}

    if "achievement" in lowered:
        steamid = ""
        text = await _call(
            "steam_stats",
            {"operation": "achievements", "steamid": steamid, "app_id": app_id},
        )
        return {"response": text, "tool": "steam_stats", "operation": "achievements"}

    if "leaderboard" in lowered:
        text = await _call("steam_stats", {"operation": "leaderboards", "app_id": app_id})
        return {"response": text, "tool": "steam_stats", "operation": "leaderboards"}

    if "review" in lowered:
        text = await _call("steam_store", {"operation": "reviews", "app_id": app_id, "count": 5})
        return {"response": text, "tool": "steam_store", "operation": "reviews"}

    if "news" in lowered:
        text = await _call("steam_store", {"operation": "news", "app_id": app_id, "count": 5})
        return {"response": text, "tool": "steam_store", "operation": "news"}

    if "workshop" in lowered:
        search = _extract_query(q) or ""
        text = await _call(
            "steam_workshop",
            {"operation": "query", "app_id": app_id, "query": search, "count": 10},
        )
        return {"response": text, "tool": "steam_workshop", "operation": "query"}

    if any(k in lowered for k in ("search", "find game", "look up game", "store")):
        search = _extract_query(q) or q.replace("search", "").replace("for", "").strip()
        if not search:
            search = "indie"
        text = await _call("steam_store", {"operation": "search", "query": search, "count": 8})
        return {"response": text, "tool": "steam_store", "operation": "search"}

    if "status" in lowered or "health" in lowered:
        text = await _call("steam_system", {"operation": "status"})
        return {"response": text, "tool": "steam_system", "operation": "status"}

    if "steamcmd" in lowered:
        text = await _call("steam_system", {"operation": "steamcmd_status"})
        return {"response": text, "tool": "steam_system", "operation": "steamcmd_status"}

    if "help" in lowered:
        text = await _call("steam_help", {"level": "full"})
        return {"response": text, "tool": "steam_help", "operation": "full"}

    search = _extract_query(q)
    if search:
        text = await _call("steam_store", {"operation": "search", "query": search, "count": 8})
        return {"response": text, "tool": "steam_store", "operation": "search"}

    text = await _call("steam_help", {"level": "brief"})
    return {
        "response": f"I didn't match a specific intent for: `{q}`\n\n{text}",
        "tool": "steam_help",
        "operation": "brief",
    }
