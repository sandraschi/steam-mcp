"""Agentic workflow (SEP-1577 sampling)."""

from __future__ import annotations

import logging
from typing import Annotated

from fastmcp import Context
from pydantic import Field

from ..registry import TOOL_VERSION, mcp

logger = logging.getLogger("steam-mcp.agentic")


@mcp.tool(version=TOOL_VERSION)
async def agentic_steam_workflow(
    goal: Annotated[str, Field(description="Natural language Steam goal, e.g. 'find Godot games and player counts'.")],
    ctx: Context,
) -> dict:
    """Plan and execute multi-step Steam queries via host LLM sampling (SEP-1577)."""
    try:
        status = await ctx.sample(
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"You are the Steam-MCP agent. Goal: {goal}\n\n"
                        "Available tools:\n"
                        "- steam_profile(operation=own|summaries|friends|resolve_vanity, …)\n"
                        "- steam_library(operation=owned|recent|details|wishlist, …)\n"
                        "- steam_stats(operation=achievements|global_percentages|players|leaderboards, …)\n"
                        "- steam_store(operation=news|search|reviews, …)\n"
                        "- steam_workshop(operation=query|item_details, …)\n"
                        "- steam_system(operation=status|steamcmd_status)\n\n"
                        "Call the minimal tools needed, then summarize results for the user."
                    ),
                }
            ],
            max_tokens=2048,
        )
        text = status.text if hasattr(status, "text") else str(status)
        return {"success": True, "message": text, "data": {"goal": goal}}
    except Exception as exc:
        logger.exception("agentic_steam_workflow failed")
        return {
            "success": False,
            "message": f"Sampling unavailable or failed: {exc}. Chain portmanteau tools manually.",
            "data": None,
        }
