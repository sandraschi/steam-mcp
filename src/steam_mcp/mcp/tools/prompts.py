"""MCP prompt templates."""

from __future__ import annotations

from ..registry import mcp


@mcp.prompt
def steam_library_review(app_id: int = 0) -> str:
    """Review a Steam library or single game — achievements, playtime, store context."""
    focus = f" for app `{app_id}`" if app_id else ""
    return (
        f"You are a Steam gaming analyst. Use steam_library and steam_stats tools{focus}. "
        "Summarize playtime, achievements, and current player activity in Markdown."
    )


@mcp.prompt
def steam_store_search(default_query: str = "indie") -> str:
    """Search the Steam store and compare concurrent player counts."""
    return (
        f"Search Steam for '{default_query}' using steam_store(operation='search'). "
        "For top hits, call steam_stats(operation='players') and steam_store(operation='reviews'). "
        "Present a ranked comparison table in Markdown."
    )


@mcp.prompt
def steam_workshop_browse(app_id: int = 440) -> str:
    """Browse Workshop items for a game with popularity sorting."""
    return (
        f"Browse Steam Workshop for app `{app_id}` using steam_workshop(operation='query'). "
        "Highlight the most subscribed items and fetch details for the top 3."
    )
