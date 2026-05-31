# -*- mode: python ; coding: utf-8 -*-
# Tauri sidecar — single-file backend (FastAPI + MCP on :11020)
from PyInstaller.building.build_main import Analysis, EXE, PYZ
from PyInstaller.utils.hooks import copy_metadata

datas = [
    ("src/steam_mcp", "src/steam_mcp"),
    ("pyproject.toml", "."),
]
for pkg in ("fastmcp", "fastapi", "uvicorn", "pydantic", "starlette", "httpx", "prefab_ui", "structlog"):
    try:
        datas += copy_metadata(pkg)
    except Exception:
        pass

a = Analysis(
    ["run_server.py"],
    pathex=["src"],
    binaries=[],
    datas=datas,
    hiddenimports=[
        "uvicorn.logging",
        "uvicorn.loops",
        "uvicorn.loops.asyncio",
        "uvicorn.protocols",
        "uvicorn.protocols.http",
        "uvicorn.protocols.http.httptools_impl",
        "uvicorn.protocols.http.h11_impl",
        "uvicorn.lifespan",
        "uvicorn.lifespan.on",
        "steam_mcp.mcp.tools.portmanteau",
        "steam_mcp.mcp.tools.prefab",
        "steam_mcp.mcp.tools.help",
        "steam_mcp.mcp.tools.agentic",
        "steam_mcp.mcp.tools.prompts",
        "steam_mcp.mcp.tools.resources",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["playwright"],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="steam-mcp-backend",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
