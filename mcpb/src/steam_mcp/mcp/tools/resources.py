"""MCP resources."""

from __future__ import annotations

from ..registry import mcp


@mcp.resource("resource://steam/capabilities")
def steam_capabilities() -> str:
    """Tool and transport capabilities for Steam-MCP."""
    return (
        "# Steam-MCP Capabilities\n\n"
        "- **Tools:** steam_profile, steam_library, steam_stats, steam_store, "
        "steam_workshop, steam_system, steam_help, agentic_steam_workflow\n"
        "- **Prefab:** show_steam_status_card, show_library_card, show_store_search_card\n"
        "- **Transport:** stdio + HTTP `/mcp` on port 11020\n"
        "- **Auth:** STEAM_API_KEY, STEAM_ID (optional for public store endpoints)\n"
    )


@mcp.resource("resource://steam/quickstart")
def steam_quickstart() -> str:
    """Quick start for Steam-MCP."""
    return (
        "# Quick Start\n\n"
        "1. Get API key: https://steamcommunity.com/dev/apikey\n"
        "2. `set STEAM_API_KEY=…` and `set STEAM_ID=…`\n"
        "3. `just serve` → http://localhost:11020/mcp\n"
        "4. Try `steam_store(operation='search', query='Godot')` without a key.\n"
    )
