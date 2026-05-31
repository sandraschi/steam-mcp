<p align="center">
  <img src="https://img.shields.io/badge/python-3.12+-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/fastmcp-3.2+-purple" alt="FastMCP">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
  <img src="https://img.shields.io/badge/version-0.2.0-blue" alt="Version">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Port_Backend-11020-blueviolet" alt="Backend Port">
  <img src="https://img.shields.io/badge/Port_Frontend-11021-blueviolet" alt="Frontend Port">
  <img src="https://img.shields.io/badge/MCP_HTTP-%2Fmcp-ff69b4" alt="MCP Path">
</p>

# Steam-MCP

**FastMCP 3.2 portmanteau server for Valve Steam** — profile, library, stats, store, Workshop, and SteamCMD status. React dashboard with tool console, Prefab cards, prompts, resources, and agentic workflow.

---

## Portmanteau tools

| Tool | Operations |
|------|------------|
| `steam_profile` | `own`, `summaries`, `friends`, `resolve_vanity` |
| `steam_library` | `owned`, `recent`, `details`, `wishlist` |
| `steam_stats` | `achievements`, `global_percentages`, `players`, `leaderboards` |
| `steam_store` | `news`, `search`, `reviews` |
| `steam_workshop` | `query`, `item_details` |
| `steam_system` | `status`, `steamcmd_status` |

Also: `steam_help`, `agentic_steam_workflow`, Prefab `show_*` cards.

No API key: store search, app details, news, player counts, global achievement %.

---

## Quick start

```powershell
git clone https://github.com/sandraschi/steam-mcp.git
cd steam-mcp
uv sync

$env:STEAM_API_KEY = "your-key"   # https://steamcommunity.com/dev/apikey
$env:STEAM_ID = "7656119xxxxxxxxxx"

just serve              # backend :11020
.\start.ps1             # backend + frontend :11021
```

MCP: `http://localhost:11020/mcp` · REST: `/api/status`, `/api/tools/{name}/call`

---

## MCP client config

```json
{
  "mcpServers": {
    "steam": {
      "command": "uv",
      "args": ["--directory", "D:/Dev/repos/steam-mcp", "run", "steam-mcp"],
      "env": {
        "STEAM_API_KEY": "...",
        "STEAM_ID": "..."
      }
    }
  }
}
```

HTTP:

```json
{
  "mcpServers": {
    "steam": { "url": "http://localhost:11020/mcp" }
  }
}
```

---

## Example calls

```json
{"operation": "search", "query": "Godot", "count": 5}
```
→ `steam_store`

```json
{"operation": "players", "app_id": 440}
```
→ `steam_stats` (no key)

```json
{"operation": "owned"}
```
→ `steam_library` (key + STEAM_ID)

---

## Architecture

```
src/steam_mcp/
  services/          # Steam API logic (shared httpx client)
  mcp/tools/         # portmanteau, prefab, prompts, resources, agentic
  skills/steam-mcp/  # MCP skill for hosts
  server.py          # FastAPI + /mcp mount
  web.py             # REST bridge
webapp/              # Vite React dashboard (Chat tool console)
```

---

## Development

```powershell
just install
just test
just smoke
just lint
just e2e
```

Fleet doc: `mcp-central-docs/projects/steam-mcp/README.md`

---

## License

MIT
