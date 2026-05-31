# Changelog

## 0.3.1 (2026-05-31)

- Fleet SOTA completion: `/.well-known/mcp/manifest.json`, `/api/capabilities`
- MCPB `assets/prompts/` (system, user, examples, workflows, troubleshooting) + `assets/icon.png`
- `install-mcp.ps1`, `.mcpbignore`, enhanced `manifest.json`
- `scripts/generate_llms_full.py`, CI MCPB artifact, release workflow (MCPB + Windows Tauri)
- Webapp `VITE_API_BASE` for Tauri production; tool versions via `TOOL_VERSION`
- `glama.json` discovery URLs; deprecated legacy `mcpb.json` stub

## 0.3.0 (2026-05-31)

- Hybrid web chat: Ollama/OpenAI-compatible LLM router + rule fallback (`STEAM_CHAT_MODE`)
- REST: `/api/llm/models`, `/api/llm/configure`
- FastMCP `SkillsDirectoryProvider` wired in server
- MCPB: `manifest.json`, `build_mcpb.py`, `just mcpb-pack`
- Tauri 2 native scaffold: sidecar spec, `native/build.ps1`, fleet-aligned layout
- Prefab: `show_workshop_card`, `STEAM_PREFAB_APPS` toggle
- Docs: expanded `llms.txt`, `llms-full.txt`, `AGENTS.md`

## 0.2.1 (2026-05-31)

- Chat orchestrator (`/api/chat`) with Ask Steam + tool console UI
- Tauri native scaffold README (deferred build)
- Fleet launcher `starts/steam-mcp-start.bat`

## 0.2.0 (2026-05-31)

- **Breaking:** Replaced 14 atomic tools with 6 portmanteau tools + help/agentic/prefab
- Added `steam_store(operation='reviews')`, `steam_library(operation='wishlist')`, `steam_workshop(operation='item_details')`
- FastMCP 3.2: prompts, resources, prefab-ui cards, `agentic_steam_workflow`
- Shared httpx client lifespan, structlog, markdown formatters
- Webapp: Chat tool console, live Games/Profile pages, Settings connectivity tests
- Fleet: `llms.txt`, `glama.json`, `mcpb.json`, CI, pytest, pre-commit
- Docs aligned with mcp-central-docs SOTA bash

## 0.1.0 (2026-05-25)

- Initial release: 14 atomic MCP tools
- FastAPI + React dashboard on ports 11020/11021
