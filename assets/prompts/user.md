# Steam-MCP — User Guide & Tutorials

This document teaches end users and agents how to accomplish common Steam tasks through steam-mcp.

## Installation

### Claude Desktop (MCPB)

1. Build or download `dist/steam-mcp.mcpb`
2. Drag the `.mcpb` file into Claude Desktop settings
3. Configure `STEAM_API_KEY` and `STEAM_ID` in the bundle user settings

### Cursor / VS Code / CLI

```powershell
cd D:\Dev\repos\steam-mcp
uv sync
.\install-mcp.ps1 cursor   # or claude, print, windsurf, zed
```

Set environment variables before starting the client:

```powershell
$env:STEAM_API_KEY = "your-key"
$env:STEAM_ID = "7656119xxxxxxxxxx"
```

### HTTP MCP (LobeHub / remote clients)

Point the client at:

```
http://127.0.0.1:11020/mcp
```

Discovery manifest:

```
http://127.0.0.1:11020/.well-known/mcp/manifest.json
```

---

## Tutorial 1: Search the store (no API key)

**Goal:** Find games matching "Godot".

**Tool:** `steam_store`

**Arguments:**

```json
{"operation": "search", "query": "Godot", "count": 8}
```

**Prefab alternative:** `show_store_search_card(query="Godot")`

---

## Tutorial 2: Live player count

**Goal:** How many people are playing Team Fortress 2 (app 440)?

**Tool:** `steam_stats`

```json
{"operation": "players", "app_id": 440}
```

**Prefab:** `show_player_count_card(app_id=440)`

---

## Tutorial 3: My owned games

**Goal:** List games on the configured account.

**Prerequisites:** `STEAM_API_KEY` + `STEAM_ID`

**Tool:** `steam_library`

```json
{"operation": "owned"}
```

Optional `steamid` overrides the default.

---

## Tutorial 4: Game details

**Goal:** Metadata for app 570 (Dota 2).

```json
{"operation": "details", "app_id": 570}
```

Works with API key; some fields are richer when authenticated.

---

## Tutorial 5: Recent news

```json
{"operation": "news", "app_id": 440, "count": 5}
```

---

## Tutorial 6: Workshop mods for TF2

```json
{"operation": "query", "app_id": 440, "query": "training", "count": 10}
```

Requires API key.

---

## Tutorial 7: Achievement progress

```json
{"operation": "achievements", "steamid": "", "app_id": 440}
```

Uses default `STEAM_ID` when `steamid` is empty.

---

## Tutorial 8: Global achievement rarity

No key required for global percentages:

```json
{"operation": "global_percentages", "app_id": 440}
```

---

## Tutorial 9: Server health

```json
{"operation": "status"}
```

Via `steam_system`. Prefab: `show_steam_status_card()`.

---

## Tutorial 10: Multi-step agentic workflow

When the host supports MCP sampling:

```
agentic_steam_workflow(goal="Search for Portal, get player counts, and summarize")
```

Without sampling, chain tools manually and summarize.

---

## Web dashboard

```powershell
just serve
.\webapp\start.ps1
```

Open `http://localhost:11021`

- **Chat:** hybrid LLM (Ollama) + rule fallback
- **Settings:** test connectivity, switch chat mode
- **Tool console:** call any portmanteau tool directly

### Ollama setup

1. Install Ollama and pull a model: `ollama pull llama3.1:8b`
2. Set `STEAM_CHAT_MODE=hybrid` (default)
3. Optional: `AI_MODEL`, `AI_ENDPOINT`

---

## Tauri native app

```powershell
.\native\build.ps1
```

Produces a Windows installer with embedded backend sidecar on port 11020.

Dev mode:

```powershell
just serve
just native-dev
```

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| "API key missing" | Set `STEAM_API_KEY` |
| Empty library | Set `STEAM_ID`; profile must be public or key must own the account |
| LLM chat falls back to rules | Start Ollama or set `STEAM_CHAT_MODE=rules` |
| MCP HTTP 404 | Use `/mcp` not `/sse`; run `just serve` |
| Prefab shows dict not card | Install `prefab-ui`; check `STEAM_PREFAB_APPS` |

See `assets/prompts/troubleshooting.md` for extended diagnostics.

---

## REST API quick reference

| Method | Path |
|--------|------|
| GET | `/api/status` |
| GET | `/api/capabilities` |
| GET | `/api/tools` |
| POST | `/api/tools/{name}/call` |
| POST | `/api/chat` |
| GET | `/.well-known/mcp/manifest.json` |

---

## Getting a Steam Web API key

1. Visit https://steamcommunity.com/dev/apikey
2. Register a domain (localhost is fine for dev)
3. Copy the key into `STEAM_API_KEY`

Never commit keys to git.
