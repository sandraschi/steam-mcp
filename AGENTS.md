# Steam-MCP Agent Context

## Repo
`steam-mcp` — FastMCP 3.2 portmanteau server for Steam profile, library, stats, store, and Workshop. **v0.3.1**

## Ports
- Backend: 11020 (FastAPI + MCP HTTP at /mcp)
- Frontend: 11021 (Vite dev; Tauri native uses same webapp)
- Env: `BACKEND_PORT`, `FRONTEND_PORT`

## Auth
- `STEAM_API_KEY` — profile, library, workshop, wishlist
- `STEAM_ID` — default account for own profile / library
- Public: store search, app details, news, player counts

## AI / chat (webapp)
- `STEAM_CHAT_MODE` — `hybrid` (default) | `llm` | `rules`
- `AI_PROVIDER`, `AI_ENDPOINT`, `AI_MODEL` — Ollama / OpenAI-compatible
- `STEAM_SAMPLING_BASE_URL` — fallback for `AI_ENDPOINT`
- `STEAM_PREFAB_APPS=0` — disable prefab-ui App tools (dict fallbacks)

## Portmanteau tools
- `steam_profile` — own | summaries | friends | resolve_vanity
- `steam_library` — owned | recent | details | wishlist
- `steam_stats` — achievements | global_percentages | players | leaderboards
- `steam_store` — news | search | reviews
- `steam_workshop` — query | item_details
- `steam_system` — status | steamcmd_status
- `steam_help`, `agentic_steam_workflow`, Prefab `show_*` cards

## Packaging
- `manifest.json` + `just mcpb-pack` → `dist/steam-mcp.mcpb`
- `glama.json`, `llms.txt`, `llms-full.txt` — discovery / LLM corpus
- `native/` — Tauri 2 + PyInstaller sidecar (`build-sidecar.ps1`, `build.ps1`)

## Layout
- `src/steam_mcp/services/` — Steam API logic
- `src/steam_mcp/mcp/tools/` — portmanteau, prefab, prompts, resources, agentic
- `src/steam_mcp/skills/steam-mcp/SKILL.md` — agent skill (also `SkillsDirectoryProvider`)

## Commands
- `just run` — STDIO MCP
- `just serve` — HTTP + REST + MCP
- `just test` / `just smoke` / `just mcpb-pack`
- `just native-dev` / `just native-build`
- `start.ps1` / `webapp/start.ps1` — full stack

Install docs: mcp-central-docs/standards/AGENT_INSTALL_REFERENCE.md
