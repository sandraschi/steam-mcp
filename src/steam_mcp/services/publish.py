from __future__ import annotations

from pathlib import Path

from ..config import settings
from ..formatters import result


async def steamcmd_status() -> dict:
    path = settings.steamcmd_path
    if not path:
        return result(
            True,
            "## SteamCMD\n\n`STEAMCMD_PATH` not set. Install steamcmd and point env var at the executable.",
            {"configured": False, "exists": False},
        )
    exists = Path(path).is_file()
    md = f"## SteamCMD\n\n- **Path:** `{path}`\n- **Exists:** {exists}"
    if exists:
        md += "\n\n**Next steps:** use SteamPipe docs in mcp-central-docs for depot upload workflows."
    return result(True, md, {"configured": True, "exists": exists, "path": path})
