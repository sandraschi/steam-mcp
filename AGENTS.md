# Steam-MCP Agent Context

## Repo
`steam-mcp` — FastMCP 3.2 portmanteau server for Steam profile, library, stats, store, and Workshop.

## Ports
- Backend: 11020 (FastAPI + MCP HTTP at /mcp)
- Frontend: 11021 (Vite dev)
- Env: `BACKEND_PORT`, `FRONTEND_PORT`

## Auth
- `STEAM_API_KEY` — profile, library, workshop, wishlist
- `STEAM_ID` — default account for own profile / library
- Public: store search, app details, news, player counts

## Portmanteau tools
- `steam_profile` — own | summaries | friends | resolve_vanity
- `steam_library` — owned | recent | details | wishlist
- `steam_stats` — achievements | global_percentages | players | leaderboards
- `steam_store` — news | search | reviews
- `steam_workshop` — query | item_details
- `steam_system` — status | steamcmd_status
- `steam_help`, `agentic_steam_workflow`, Prefab `show_*` cards

## Layout
- `src/steam_mcp/services/` — Steam API logic
- `src/steam_mcp/mcp/tools/` — portmanteau, prefab, prompts, resources, agentic
- `src/steam_mcp/skills/steam-mcp/SKILL.md` — agent skill

## Commands
- `just run` — STDIO
- `just serve` — HTTP + REST
- `just test` — pytest
- `start.ps1` / `webapp/start.ps1` — full stack

Install docs: mcp-central-docs/standards/AGENT_INSTALL_REFERENCE.md
