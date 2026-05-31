# Changelog

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
