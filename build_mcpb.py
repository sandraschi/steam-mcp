"""Build the MCPB package for steam-mcp (Claude Desktop drag-and-drop install)."""

import json
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
MANIFEST = ROOT / "manifest.json"
SERVER_DIR = ROOT / "src" / "steam_mcp"
SKILLS_DIR = SERVER_DIR / "skills"

INCLUDE_EXTS = {".py", ".md", ".txt", ".json", ".toml"}
EXCLUDE_DIRS = {"__pycache__", ".git", ".venv", "node_modules"}


def build() -> str:
    DIST.mkdir(parents=True, exist_ok=True)
    out_path = DIST / "steam-mcp.mcpb"

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    with tarfile.open(out_path, "w:gz") as tar:
        tar.add(MANIFEST, arcname="manifest.json")

        for f in SERVER_DIR.rglob("*"):
            if f.is_dir() and f.name in EXCLUDE_DIRS:
                continue
            if f.is_file() and f.suffix in INCLUDE_EXTS:
                arc = f.relative_to(ROOT).as_posix()
                tar.add(f, arcname=arc)

        readme = ROOT / "README.md"
        if readme.exists():
            tar.add(readme, arcname="README.md")

        license_file = ROOT / "LICENSE"
        if license_file.exists():
            tar.add(license_file, arcname="LICENSE")

    size = out_path.stat().st_size
    print(f"Built {out_path.name} ({size / 1024:.0f} KB)")
    print(f"  Server: steam-mcp v{manifest.get('version', '?.?.?')}")
    print(f"  Tools:  {len(manifest.get('tools', []))}")
    return str(out_path)


if __name__ == "__main__":
    build()
