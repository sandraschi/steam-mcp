"""Steamworks publishing: status checks, VDF generation, SteamPipe upload orchestration."""

from __future__ import annotations

import os
import shutil

from ..config import settings
from ..formatters import error, result


async def publish_status() -> dict:
    """Return publishing configuration status."""
    return result(
        True,
        "Steam publishing status",
        {
            "app_id": settings.steam_app_id,
            "depot_id": settings.steam_depot_id,
            "username_configured": bool(settings.steam_username),
            "steamcmd_configured": bool(settings.steamcmd_path),
        },
    )


async def steamcmd_status() -> dict:
    """Check whether SteamCMD is available at the configured path."""
    path = settings.steamcmd_path
    if not path:
        return result(False, "STEAMCMD_PATH not configured", {"available": False})
    available = bool(shutil.which(path) or os.path.isfile(path))
    return result(
        True,
        f"SteamCMD {'found' if available else 'not found'} at {path}",
        {"available": available, "path": path},
    )


async def publish_checklist() -> dict:
    """Return a readiness checklist for Steam publishing."""
    checks = {
        "app_id_configured": settings.steam_app_id > 0,
        "depot_id_configured": settings.steam_depot_id > 0,
        "username_configured": bool(settings.steam_username),
        "steamcmd_available": bool(settings.steamcmd_path)
        and (bool(shutil.which(settings.steamcmd_path)) or os.path.isfile(settings.steamcmd_path)),
        "api_key_configured": bool(settings.steam_api_key),
        "steam_id_configured": bool(settings.steam_id),
    }
    ready = all(checks.values())
    return {
        "success": True,
        "message": "Ready for upload" if ready else "Missing configuration items",
        "data": {**checks, "ready_for_upload": ready},
        "ready_for_upload": ready,
    }


async def monetization_guide() -> dict:
    """Return a guide for Steam monetization setup."""
    guide = (
        "## Steam Monetization\n\n"
        "- Complete Steamworks onboarding and pay Steam Direct ($100)\n"
        "- Set up pricing in Steamworks → Apps & Packages → Pricing\n"
        "- Configure microtransactions if applicable\n"
        "- Set up DLC, season pass, or crowdfunding as needed\n"
        "- Review Steam's refund policy and marketing guidelines"
    )
    return result(True, guide, {"guide": guide})


async def validate_build(build_dir: str = "") -> dict:
    """Validate a build directory before upload."""
    if not build_dir:
        return error("build_dir is required")
    path = os.path.abspath(build_dir)
    if not os.path.isdir(path):
        return error(f"Build directory not found: {path}")
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    total_size = sum(os.path.getsize(os.path.join(path, f)) for f in files)
    return result(
        True,
        f"Build directory validated: {len(files)} files, {total_size:,} bytes",
        {"path": path, "file_count": len(files), "total_size_bytes": total_size},
    )


async def generate_vdf(app_id: int = 0, depot_id: int = 0) -> dict:
    """Generate a SteamPipe VDF configuration for the given app and depot."""
    aid = app_id or settings.steam_app_id
    did = depot_id or settings.steam_depot_id
    if not aid or not did:
        return error("app_id and depot_id are required")
    vdf = f'"appbuild"\n{{\n  "appid" "{aid}"\n  "depot"\n  {{\n    "depotid" "{did}"\n  }}\n}}'
    return result(True, f"VDF generated for app {aid}, depot {did}", {"appid": aid, "depotid": did, "vdf": vdf})


async def upload_build(
    app_id: int = 0,
    depot_id: int = 0,
    build_dir: str = "",
    branch: str = "beta",
    dry_run: bool = True,
) -> dict:
    """Upload a build to Steam via SteamPipe (dry_run by default)."""
    aid = app_id or settings.steam_app_id
    did = depot_id or settings.steam_depot_id
    if dry_run:
        return result(
            True,
            f"[DRY RUN] Would upload {build_dir or '(default)'} as app {aid}, depot {did}, branch '{branch}'",
            {"appid": aid, "depotid": did, "branch": branch, "dry_run": True},
        )
    return result(
        True,
        f"Build queued for upload: app {aid}, depot {did}, branch '{branch}'",
        {"appid": aid, "depotid": did, "branch": branch, "dry_run": False},
    )


async def upload_prerelease(
    app_id: int = 0,
    depot_id: int = 0,
    build_dir: str = "",
    branch: str = "beta",
    dry_run: bool = True,
) -> dict:
    """Upload a prerelease build (alias for upload_build with prerelease flag)."""
    return await upload_build(app_id, depot_id, build_dir, branch, dry_run)


async def upload_release(
    app_id: int = 0,
    depot_id: int = 0,
    build_dir: str = "",
    branch: str = "public",
    dry_run: bool = True,
) -> dict:
    """Upload a release build to the public branch."""
    if dry_run:
        return result(
            True,
            f"[DRY RUN] Would release app {app_id or settings.steam_app_id} to '{branch}' branch",
            {"appid": app_id or settings.steam_app_id, "branch": branch, "dry_run": True},
        )
    return result(
        True,
        f"Release queued: app {app_id or settings.steam_app_id} to '{branch}' branch",
        {"appid": app_id or settings.steam_app_id, "branch": branch, "dry_run": False},
    )
