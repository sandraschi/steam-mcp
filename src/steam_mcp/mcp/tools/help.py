"""Help and discovery tools."""

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import Field

from ..registry import mcp

HelpLevel = Literal["brief", "full", "operations"]


@mcp.tool(version="0.2.0")
async def steam_help(
    level: Annotated[HelpLevel, Field(description="Help depth: brief, full, or operations.")] = "brief",
) -> dict:
    """Multi-level help for Steam-MCP portmanteau tools and auth requirements."""
    if level == "brief":
        text = (
            "## Steam-MCP\n\n"
            "Portmanteau tools: `steam_profile`, `steam_library`, `steam_stats`, "
            "`steam_store`, `steam_workshop`, `steam_system`, `steam_help`, "
            "`agentic_steam_workflow`.\n\n"
            "Set `STEAM_API_KEY` + `STEAM_ID` for profile/library. "
            "Store player counts work without a key."
        )
    elif level == "operations":
        text = (
            "## Operations\n\n"
            "- **steam_profile:** own | summaries | friends | resolve_vanity\n"
            "- **steam_library:** owned | recent | details | wishlist\n"
            "- **steam_stats:** achievements | global_percentages | players | leaderboards\n"
            "- **steam_store:** news | search | reviews\n"
            "- **steam_workshop:** query | item_details\n"
            "- **steam_system:** status | steamcmd_status"
        )
    else:
        text = (
            "## Steam-MCP Full Help\n\n"
            "Backend :11020, frontend :11021, MCP at `/mcp`.\n\n"
            "Resources: `resource://steam/capabilities`, `resource://steam/quickstart`.\n\n"
            "Prefab: `show_steam_status_card`, `show_library_card`, `show_store_search_card`.\n\n"
            "Agentic: `agentic_steam_workflow(goal='…')` when host supports sampling."
        )
    return {"success": True, "message": text, "data": {"level": level}}
