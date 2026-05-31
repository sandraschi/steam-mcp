# steam-mcp — Claude Code Guide

## Overview
MCP server for Steam — portmanteau tools on ports 11020/11021.

## Entry Points
- `uv run steam-mcp` → stdio
- `just serve` → FastAPI + `/mcp`

## Standards
- FastMCP 3.2+ **portmanteau** tools with `operation` enum
- Markdown in `message` field; structured data in `data`
- prefab-ui, prompts, resources, agentic sampling (SEP-1577)
- See mcp-central-docs for fleet standards

## Key Files
- `src/steam_mcp/services/` — API layer
- `src/steam_mcp/mcp/tools/portmanteau.py` — main tools
- `README.md`, `AGENTS.md`, `skills/steam-mcp/SKILL.md`
