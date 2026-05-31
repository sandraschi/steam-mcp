"""Build the MCPB package for steam-mcp (Claude Desktop drag-and-drop install)."""

import json
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
MANIFEST = ROOT / "manifest.json"
SERVER_DIR = ROOT / "src" / "steam_mcp"
ASSETS_DIR = ROOT / "assets"

INCLUDE_EXTS = {".py", ".md", ".txt", ".json", ".toml", ".png", ".svg", ".ico"}
EXCLUDE_DIRS = {"__pycache__", ".git", ".venv", "node_modules"}


def _validate_manifest() -> dict:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if not (ASSETS_DIR / "icon.png").is_file():
        raise FileNotFoundError("assets/icon.png required for MCPB")
    for prompt in ("system.md", "user.md", "examples.json"):
        if not (ASSETS_DIR / "prompts" / prompt).is_file():
            raise FileNotFoundError(f"assets/prompts/{prompt} required for MCPB")
    return manifest


def _pack_tar(out_path: Path, manifest: dict) -> None:
    with tarfile.open(out_path, "w:gz") as tar:
        tar.add(MANIFEST, arcname="manifest.json")
        for f in SERVER_DIR.rglob("*"):
            if f.is_dir() and f.name in EXCLUDE_DIRS:
                continue
            if f.is_file() and f.suffix in INCLUDE_EXTS:
                tar.add(f, arcname=f.relative_to(ROOT).as_posix())
        for f in ASSETS_DIR.rglob("*"):
            if f.is_file() and f.suffix in INCLUDE_EXTS:
                tar.add(f, arcname=f.relative_to(ROOT).as_posix())
        readme = ROOT / "README.md"
        if readme.exists():
            tar.add(readme, arcname="README.md")
        changelog = ROOT / "CHANGELOG.md"
        if changelog.exists():
            tar.add(changelog, arcname="CHANGELOG.md")


def _pack_mcpb_cli(out_path: Path) -> bool:
    mcpb = shutil.which("mcpb")
    if not mcpb:
        return False
    DIST.mkdir(parents=True, exist_ok=True)
    subprocess.run([mcpb, "pack", str(ROOT), str(out_path)], check=True)
    return True


def build() -> str:
    DIST.mkdir(parents=True, exist_ok=True)
    manifest = _validate_manifest()
    version = manifest.get("version", "0.0.0")
    out_cli = DIST / f"steam-mcp-v{version}.mcpb"
    out_tar = DIST / "steam-mcp.mcpb"

    if _pack_mcpb_cli(out_cli):
        out_path = out_cli
    else:
        _pack_tar(out_tar, manifest)
        out_path = out_tar

    size = out_path.stat().st_size
    print(f"Built {out_path.name} ({size / 1024:.0f} KB)")
    print(f"  Server: steam-mcp v{version}")
    print(f"  Tools:  {len(manifest.get('tools', []))}")
    return str(out_path)


if __name__ == "__main__":
    try:
        build()
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
