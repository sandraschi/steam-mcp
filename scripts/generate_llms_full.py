#!/usr/bin/env python3
"""Regenerate llms-full.txt from repo docs (fleet LLM corpus)."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "llms-full.txt"

SECTIONS = [
    ("README", ROOT / "README.md"),
    ("AGENTS", ROOT / "AGENTS.md"),
    ("CHANGELOG", ROOT / "CHANGELOG.md"),
    ("Skill", ROOT / "src" / "steam_mcp" / "skills" / "steam-mcp" / "SKILL.md"),
    ("MCPB system prompt", ROOT / "assets" / "prompts" / "system.md"),
    ("MCPB user guide", ROOT / "assets" / "prompts" / "user.md"),
    ("Workflows", ROOT / "assets" / "prompts" / "workflows.md"),
]


def main() -> None:
    lines = [
        "# steam-mcp — full LLM corpus",
        "> Auto-generated. Run: uv run python scripts/generate_llms_full.py",
        "",
        f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}",
        "",
    ]
    for title, path in SECTIONS:
        lines.append(f"## {title}")
        lines.append(f"Source: `{path.relative_to(ROOT).as_posix()}`")
        lines.append("```")
        if path.is_file():
            lines.append(path.read_text(encoding="utf-8").strip())
        else:
            lines.append(f"(missing: {path})")
        lines.append("```")
        lines.append("")
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT} ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
