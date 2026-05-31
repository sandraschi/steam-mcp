"""Entry point for PyInstaller-bundled steam-mcp backend (Tauri sidecar)."""

import os
import sys

sys.path.insert(0, ".")
if getattr(sys, "frozen", False):
    meipass = getattr(sys, "_MEIPASS", "")
    if meipass:
        os.environ.setdefault("STEAM_MCP_REPO_ROOT", meipass)

from steam_mcp.transport import run_server
from steam_mcp.mcp.registry import mcp

if __name__ == "__main__":
    run_server(mcp, "steam-mcp")
