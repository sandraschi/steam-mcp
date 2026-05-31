"""Prefab UI cards for list/status tools."""

from __future__ import annotations

import logging
from typing import Annotated

from pydantic import Field

from ...config import settings
from ...services import library, stats, store, workshop
from ..registry import mcp

logger = logging.getLogger("steam-mcp.prefab")

_PREFAB = settings.prefab_apps
try:
    if _PREFAB:
        from prefab_ui.app import PrefabApp
        from prefab_ui.components import Column, Heading, Metric, Row, Text

        _PREFAB_UI = True
    else:
        _PREFAB_UI = False
except ImportError:
    _PREFAB_UI = False
    logger.info("prefab-ui not installed — using plain dict fallbacks")


def _plain_status() -> dict:
    return {
        "success": True,
        "message": (
            f"Steam-MCP status: API key {'OK' if settings.has_api_key else 'missing'}, "
            f"Steam ID {'OK' if settings.has_steam_id else 'not set'}"
        ),
        "data": {"has_api_key": settings.has_api_key, "has_steam_id": settings.has_steam_id},
    }


if _PREFAB_UI:

    @mcp.tool(app=True, version="0.3.0")
    async def show_steam_status_card() -> PrefabApp:
        """Prefab card: Steam-MCP connectivity and auth status."""
        with Column(gap=3) as view:
            Heading("Steam-MCP Status")
            Row(
                Metric(label="API Key", value="OK" if settings.has_api_key else "Missing"),
                Metric(label="Steam ID", value="Set" if settings.has_steam_id else "Unset"),
                Metric(label="Version", value="0.3.0"),
            )
        return PrefabApp(view=view, title="Steam-MCP Status")

    @mcp.tool(app=True, version="0.3.0")
    async def show_library_card(
        steamid: Annotated[str, Field(description="Steam ID; defaults to STEAM_ID.")] = "",
    ) -> PrefabApp | dict:
        """Prefab card: owned games summary (requires API key)."""
        res = await library.get_owned_games(steamid)
        if not res.get("success"):
            return res
        games = (res.get("data") or {}).get("games", [])
        with Column(gap=2) as view:
            Heading("Owned Games")
            for g in games[:12]:
                Text(f"{g.get('name', g.get('appid'))} — {(g.get('playtime_forever') or 0) // 60}h")
        return PrefabApp(view=view, title="Steam Library")

    @mcp.tool(app=True, version="0.3.0")
    async def show_store_search_card(
        query: Annotated[str, Field(description="Store search query.")] = "Godot",
    ) -> PrefabApp | dict:
        """Prefab card: Steam store search results."""
        res = await store.search_store(query, 8)
        if not res.get("success"):
            return res
        results = (res.get("data") or {}).get("results", [])
        with Column(gap=2) as view:
            Heading(f"Search: {query}")
            for r in results:
                Text(f"{r.get('name')} ({r.get('appid')})")
        return PrefabApp(view=view, title="Steam Store Search")

    @mcp.tool(app=True, version="0.3.0")
    async def show_workshop_card(app_id: int = 440, query: str = "") -> PrefabApp | dict:
        """Prefab card: Steam Workshop search results."""
        res = await workshop.query_workshop_items(app_id, query, 8)
        if not res.get("success"):
            return res
        items = (res.get("data") or {}).get("items", [])
        with Column(gap=2) as view:
            Heading(f"Workshop — app {app_id}")
            for item in items[:10]:
                Text(f"{item.get('title', '?')} ({item.get('publishedfileid')})")
        return PrefabApp(view=view, title="Steam Workshop")

    @mcp.tool(app=True, version="0.3.0")
    async def show_player_count_card(app_id: int = 440) -> PrefabApp | dict:
        """Prefab card: current in-game player count."""
        res = await stats.get_number_of_current_players(app_id)
        if not res.get("success"):
            return res
        count = (res.get("data") or {}).get("player_count", 0)
        with Column(gap=2) as view:
            Heading(f"App {app_id}")
            Metric(label="Players now", value=str(count))
        return PrefabApp(view=view, title="Steam Player Count")

else:

    @mcp.tool(version="0.3.0")
    async def show_steam_status_card() -> dict:
        """Status summary (install prefab-ui for App UI)."""
        return _plain_status()

    @mcp.tool(version="0.3.0")
    async def show_library_card(steamid: str = "") -> dict:
        """Library summary plain-text fallback."""
        return await library.get_owned_games(steamid)

    @mcp.tool(version="0.3.0")
    async def show_store_search_card(query: str = "Godot") -> dict:
        """Store search plain-text fallback."""
        return await store.search_store(query, 8)

    @mcp.tool(version="0.3.0")
    async def show_workshop_card(app_id: int = 440, query: str = "") -> dict:
        """Workshop search plain-text fallback."""
        return await workshop.query_workshop_items(app_id, query, 8)

    @mcp.tool(version="0.3.0")
    async def show_player_count_card(app_id: int = 440) -> dict:
        """Current player count plain-text fallback."""
        return await stats.get_number_of_current_players(app_id)
