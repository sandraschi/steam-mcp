"""Steamworks publishing configuration (partner / SteamPipe)."""

from __future__ import annotations

import os
from pathlib import Path

DEFAULT_EXCHANGE = Path("D:/Dev/repos/_exchange")


def steam_app_id() -> int:
    raw = os.getenv("STEAM_APP_ID", "").strip()
    if not raw:
        return 0
    return int(raw)


def steam_depot_id() -> int:
    raw = os.getenv("STEAM_DEPOT_ID", "").strip()
    if not raw:
        return 0
    return int(raw)


def steam_build_id() -> str:
    return os.getenv("STEAM_BUILD_ID", "1").strip() or "1"


def steam_username() -> str:
    return os.getenv("STEAM_USERNAME", "").strip()


def steamcmd_path() -> str:
    return os.getenv("STEAMCMD_PATH", "").strip()


def steam_branch() -> str:
    return os.getenv("STEAM_BRANCH", "beta").strip() or "beta"


def exchange_root() -> Path:
    return Path(os.getenv("FLEET_EXCHANGE_ROOT", str(DEFAULT_EXCHANGE))).resolve()


def content_root(app_id: int | None = None) -> Path:
    override = os.getenv("STEAM_CONTENT_ROOT", "").strip()
    if override:
        return Path(override).resolve()
    aid = app_id or steam_app_id()
    if not aid:
        return exchange_root() / "steam-builds" / "content"
    return exchange_root() / "steam-builds" / str(aid) / "content"


def scripts_root(app_id: int | None = None) -> Path:
    aid = app_id or steam_app_id()
    if not aid:
        return exchange_root() / "steam-builds" / "scripts"
    return exchange_root() / "steam-builds" / str(aid) / "scripts"


def build_output_root(app_id: int | None = None) -> Path:
    aid = app_id or steam_app_id()
    if not aid:
        return exchange_root() / "steam-builds" / "output"
    return exchange_root() / "steam-builds" / str(aid) / "output"


def steam_mcp_url() -> str:
    return os.getenv("STEAM_MCP_URL", "http://127.0.0.1:11020").rstrip("/")
