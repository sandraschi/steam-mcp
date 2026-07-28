"""Portmanteau MCP tools for Steam API access."""

from __future__ import annotations

from typing import Annotated, Any, Literal

from pydantic import Field

from ... import __version__ as _server_version
from ...services import library, profile, stats, store, workshop
from ..registry import TOOL_VERSION, mcp

ProfileOp = Literal["own", "summaries", "friends", "resolve_vanity"]
LibraryOp = Literal["owned", "recent", "details", "wishlist"]
StatsOp = Literal["achievements", "global_percentages", "players", "leaderboards"]
StoreOp = Literal["news", "search", "reviews"]
WorkshopOp = Literal["query", "item_details"]
SystemOp = Literal["status", "steamcmd_status"]


@mcp.tool(version=TOOL_VERSION)
async def steam_profile(
    operation: Annotated[
        ProfileOp, Field(description="Profile operation: own, summaries, friends, or resolve_vanity.")
    ],
    steamid: Annotated[str, Field(description="64-bit Steam ID required for friends.")] = "",
    steamids: Annotated[str, Field(description="Comma-separated Steam IDs for summaries (up to 100).")] = "",
    vanity_url: Annotated[
        str, Field(description="Vanity URL slug, e.g. 'sandraschi' from steamcommunity.com/id/sandraschi.")
    ] = "",
    relationship: Annotated[str, Field(description="Friend filter: 'all' or 'friend'.")] = "all",
) -> dict[str, Any]:
    """Query player profiles: own profile, summaries, friend list, vanity URL resolution. Requires STEAM_API_KEY."""
    if operation == "own":
        return await profile.get_own_profile()
    if operation == "summaries":
        target = steamids or steamid
        if not target:
            return {"success": False, "message": "Provide steamids or steamid", "data": None}
        return await profile.get_player_summaries(target)
    if operation == "friends":
        if not steamid:
            return {"success": False, "message": "steamid required for friends", "data": None}
        return await profile.get_friend_list(steamid, relationship)
    if operation == "resolve_vanity":
        if not vanity_url:
            return {"success": False, "message": "vanity_url required", "data": None}
        return await profile.resolve_vanity_url(vanity_url)
    return {"success": False, "message": f"Unknown operation: {operation}", "data": None}


@mcp.tool(version=TOOL_VERSION)
async def steam_library(
    operation: Annotated[LibraryOp, Field(description="Library operation: owned, recent, details, or wishlist.")],
    steamid: Annotated[str, Field(description="64-bit Steam ID; defaults to STEAM_ID.")] = "",
    app_id: Annotated[int, Field(description="Steam App ID, required for details.")] = 0,
    include_free: Annotated[bool, Field(description="Include free games in owned results.")] = False,
    count: Annotated[int, Field(description="Max items for recent.", ge=1, le=50)] = 10,
    country: Annotated[str, Field(description="Country code for pricing, e.g. US, DE, GB.")] = "US",
) -> dict[str, Any]:
    """Access library: owned games, recently played, store details, wishlist. Requires API key and Steam ID."""
    if operation == "owned":
        return await library.get_owned_games(steamid, include_free)
    if operation == "recent":
        return await library.get_recently_played_games(steamid, count)
    if operation == "details":
        if not app_id:
            return {"success": False, "message": "app_id required for details", "data": None}
        return await library.get_app_details(app_id, country)
    if operation == "wishlist":
        return await library.get_wishlist(steamid)
    return {"success": False, "message": f"Unknown operation: {operation}", "data": None}


@mcp.tool(version=TOOL_VERSION)
async def steam_stats(
    operation: Annotated[
        StatsOp, Field(description="Stats operation: achievements, global_percentages, players, or leaderboards.")
    ],
    steamid: Annotated[str, Field(description="64-bit Steam ID, required for achievements.")] = "",
    app_id: Annotated[int, Field(description="Steam App ID, required for all operations.")] = 0,
) -> dict[str, Any]:
    """Stats: achievements, global rarity, concurrent players, leaderboards. Player count and global % need no key."""
    if operation == "achievements":
        if not steamid or not app_id:
            return {"success": False, "message": "steamid and app_id required", "data": None}
        return await stats.get_player_achievements(steamid, app_id)
    if operation == "global_percentages":
        if not app_id:
            return {"success": False, "message": "app_id required", "data": None}
        return await stats.get_global_achievement_percentages(app_id)
    if operation == "players":
        if not app_id:
            return {"success": False, "message": "app_id required", "data": None}
        return await stats.get_number_of_current_players(app_id)
    if operation == "leaderboards":
        if not app_id:
            return {"success": False, "message": "app_id required", "data": None}
        return await stats.get_game_leaderboards(app_id)
    return {"success": False, "message": f"Unknown operation: {operation}", "data": None}


@mcp.tool(version=TOOL_VERSION)
async def steam_store(
    operation: Annotated[StoreOp, Field(description="Store operation: news, search, or reviews.")],
    app_id: Annotated[int, Field(description="Steam App ID, required for news and reviews.")] = 0,
    query: Annotated[str, Field(description="Search query, e.g. 'Godot', 'Half-Life'.")] = "",
    count: Annotated[int, Field(description="Max results.", ge=1, le=50)] = 10,
) -> dict[str, Any]:
    """Search the Steam store, read latest news, or fetch user reviews with scores. No STEAM_API_KEY required."""
    if operation == "news":
        if not app_id:
            return {"success": False, "message": "app_id required for news", "data": None}
        return await store.get_news_for_app(app_id, count)
    if operation == "search":
        if not query:
            return {"success": False, "message": "query required for search", "data": None}
        return await store.search_store(query, count)
    if operation == "reviews":
        if not app_id:
            return {"success": False, "message": "app_id required for reviews", "data": None}
        return await store.get_app_reviews(app_id, count)
    return {"success": False, "message": f"Unknown operation: {operation}", "data": None}


@mcp.tool(version=TOOL_VERSION)
async def steam_workshop(
    operation: Annotated[WorkshopOp, Field(description="Workshop operation: query or item_details.")],
    app_id: Annotated[int, Field(description="Steam App ID for query, e.g. 440 (TF2).")] = 0,
    query: Annotated[str, Field(description="Workshop search text.")] = "",
    count: Annotated[int, Field(description="Max items.", ge=1, le=100)] = 20,
    sort_by: Annotated[
        str,
        Field(description="Sort: mostrecent, score, trend, mostsubscribed, mostfavorited."),
    ] = "mostsubscribed",
    published_file_ids: Annotated[str, Field(description="Comma-separated file IDs for item_details.")] = "",
) -> dict[str, Any]:
    """Browse Workshop mods by game with popularity sorting, or fetch published file details. Requires STEAM_API_KEY."""
    if operation == "query":
        if not app_id:
            return {"success": False, "message": "app_id required for query", "data": None}
        return await workshop.query_workshop_items(app_id, query, count, sort_by)
    if operation == "item_details":
        return await workshop.get_workshop_item_details(published_file_ids)
    return {"success": False, "message": f"Unknown operation: {operation}", "data": None}


@mcp.tool(version=TOOL_VERSION)
async def steam_system(
    operation: Annotated[SystemOp, Field(description="System operation: status (server health) or steamcmd_status.")],
) -> dict[str, Any]:
    """Check server health (API key, Steam ID, tool count) and SteamCMD binary detection for publishing."""
    from ...config import settings
    from ..registry import mcp as mcp_instance

    if operation == "status":
        tools = await mcp_instance.list_tools()
        from ...formatters import status_md

        md = status_md(settings.has_api_key, settings.has_steam_id, len(tools))
        return {
            "success": True,
            "message": md,
            "data": {
                "has_api_key": settings.has_api_key,
                "has_steam_id": settings.has_steam_id,
                "tool_count": len(tools),
                "version": _server_version,
            },
        }
    if operation == "steamcmd_status":
        from ...services.publish import steamcmd_status

        return await steamcmd_status()
    return {"success": False, "message": f"Unknown operation: {operation}", "data": None}
