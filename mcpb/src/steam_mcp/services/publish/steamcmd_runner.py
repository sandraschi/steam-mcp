"""SteamCMD execution for SteamPipe uploads."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

from ...formatters import result
from . import config


async def steamcmd_status() -> dict:
    path = config.steamcmd_path()
    if not path:
        return result(
            True,
            "## SteamCMD\n\n`STEAMCMD_PATH` not set. Install SteamCMD and point env var at the executable.",
            {"configured": False, "exists": False},
        )
    exists = Path(path).is_file()
    md = f"## SteamCMD\n\n- **Path:** `{path}`\n- **Exists:** {exists}"
    if exists:
        md += "\n\nReady for `steam_publish(operation='upload_build')` after VDF generation."
    return result(True, md, {"configured": True, "exists": exists, "path": path})


def validate_content(content_root: Path) -> dict:
    root = content_root.resolve()
    if not root.is_dir():
        return {"success": False, "error": f"Content root not found: {root}"}
    files = list(root.rglob("*"))
    file_count = sum(1 for f in files if f.is_file())
    if file_count == 0:
        return {"success": False, "error": f"No files under content root: {root}"}
    exe_files = [f for f in files if f.suffix.lower() == ".exe"]
    return {
        "success": True,
        "content_root": str(root),
        "file_count": file_count,
        "exe_count": len(exe_files),
        "has_windows_exe": len(exe_files) > 0,
    }


def run_app_build(
    app_build_vdf: str,
    *,
    dry_run: bool = False,
    timeout: int = 3600,
) -> dict:
    steamcmd = config.steamcmd_path()
    username = config.steam_username()
    vdf = Path(app_build_vdf).resolve()

    if not steamcmd or not Path(steamcmd).is_file():
        return {"success": False, "error": "STEAMCMD_PATH not configured or missing"}
    if not username:
        return {"success": False, "error": "STEAM_USERNAME required for steamcmd login"}
    if not vdf.is_file():
        return {"success": False, "error": f"app_build VDF not found: {vdf}"}

    if dry_run:
        return {
            "success": True,
            "dry_run": True,
            "command": _build_command(steamcmd, username, vdf),
            "app_build_vdf": str(vdf),
            "note": "Set dry_run=false and STEAMCMD_PASSWORD (or steam guard) to execute",
        }

    password = os.getenv("STEAMCMD_PASSWORD", "").strip()
    cmd = _build_command(steamcmd, username, vdf, password=password)
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(vdf.parent),
        )
    except subprocess.TimeoutExpired:
        return {"success": False, "error": f"steamcmd timed out after {timeout}s"}
    except OSError as exc:
        return {"success": False, "error": str(exc)}

    ok = proc.returncode == 0
    return {
        "success": ok,
        "returncode": proc.returncode,
        "stdout": (proc.stdout or "")[-4000:],
        "stderr": (proc.stderr or "")[-4000:],
        "app_build_vdf": str(vdf),
        "error": None if ok else (proc.stderr or proc.stdout or "steamcmd failed")[:500],
    }


def _build_command(steamcmd: str, username: str, vdf: Path, password: str = "") -> list[str]:
    args = [steamcmd, "+login", username]
    if password:
        args.append(password)
    args.extend(["+run_app_build", str(vdf), "+quit"])
    return args
