# Steam-MCP Agent Context

## Repo
`steam-mcp` — MCP server for Steam profile, library, stats, store, and Workshop.

## Ports
- Backend: 11020 (FastAPI + MCP HTTP at /mcp)
- Frontend: 11021 (Vite dev)
- Config via `BACKEND_PORT`, `FRONTEND_PORT` env vars

## Auth
- `STEAM_API_KEY` env var (get from steamcommunity.com/dev/apikey)
- `STEAM_ID` env var (your 64-bit Steam ID)
- Some tools work without auth (store, news, player counts)

## Package
- `src/steam_mcp/` — Python package
- `mcp/registry.py` — shared FastMCP instance
- `mcp/tools/` — tool implementations (profile, library, stats, store, workshop)
- `server.py` — FastAPI app + MCP mount, CLI entry
- `transport.py` — STDIO/HTTP transport selection

## Commands
- `just run` — STDIO mode
- `just serve` — HTTP SSE + REST on 11020
- `just frontend-dev` — Vite on 11021
- `start.ps1` — full stack launcher

## Tool Registration
FastMCP registers tools at import time via @mcp.tool decorator.
Portmanteau imports in `mcp/tools/__init__.py` must list all tool modules.
