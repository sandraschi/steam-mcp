"""Fleet discovery: well-known manifest and /api/capabilities."""

from __future__ import annotations

import json
from typing import Any

from . import __version__
from .config import settings
from .mcp.registry import mcp


def _load_manifest() -> dict[str, Any]:
    path = settings.repo_root / "manifest.json"
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"name": "steam-mcp", "version": __version__}


def build_well_known_manifest() -> dict[str, Any]:
    """LobeHub / fleet discovery manifest with HTTP + stdio transports."""
    base = _load_manifest()
    host = settings.host
    port = settings.backend_port
    http_mcp = f"http://{host}:{port}/mcp"
    return {
        "schema_version": "1.0",
        **base,
        "repository": {
            "type": "git",
            "url": "https://github.com/sandraschi/steam-mcp",
        },
        "mcp": {
            "http_url": http_mcp,
            "transports": [
                {
                    "type": "stdio",
                    "command": "uv",
                    "args": ["run", "--directory", str(settings.repo_root), "steam-mcp"],
                },
                {
                    "type": "stdio",
                    "command": "python",
                    "args": ["-m", "steam_mcp.server", "--stdio"],
                },
                {"type": "http", "url": http_mcp},
            ],
        },
        "endpoints": {
            "health": "/health",
            "status": "/api/status",
            "capabilities": "/api/capabilities",
            "tools": "/api/tools",
            "chat": "/api/chat",
            "manifest": "/.well-known/mcp/manifest.json",
        },
        "prompts": {
            "system": "assets/prompts/system.md",
            "user": "assets/prompts/user.md",
            "examples": "assets/prompts/examples.json",
        },
    }


async def build_capabilities() -> dict[str, Any]:
    tools = await mcp.list_tools()
    tool_names = sorted(t.name for t in tools)
    llm_tools = [n for n in tool_names if n.startswith("show_")]
    return {
        "status": "ok",
        "server": {"name": "steam-mcp", "version": __version__, "fastmcp": "3.2.0"},
        "tools": {"count": len(tool_names), "names": tool_names},
        "auth": {
            "has_api_key": settings.has_api_key,
            "has_steam_id": settings.has_steam_id,
        },
        "features": {
            "prefab_apps": settings.prefab_apps,
            "prefab_tools": llm_tools,
            "sampling": True,
            "skills": True,
            "prompts": True,
            "resources": True,
            "llm_chat": settings.chat_mode in ("hybrid", "llm", "rules"),
            "chat_mode": settings.chat_mode,
        },
        "endpoints": build_well_known_manifest()["endpoints"],
        "mcp": build_well_known_manifest()["mcp"],
    }
