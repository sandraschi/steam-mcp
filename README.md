<p align="center">
  <img src="https://img.shields.io/badge/python-3.12+-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/fastmcp-3.2+-purple" alt="FastMCP">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
  <img src="https://img.shields.io/github/v/release/sandraschi/steam-mcp" alt="Release">
  <img src="https://img.shields.io/badge/status-active-brightgreen" alt="Status">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Port_Backend-11020-blueviolet" alt="Backend Port">
  <img src="https://img.shields.io/badge/Port_Frontend-11021-blueviolet" alt="Frontend Port">
  <img src="https://img.shields.io/badge/MCP_HTTP-%2Fmcp-ff69b4" alt="MCP Path">
</p>

# Steam-MCP

**MCP server for Valve's Steam** — query your game library, player profile, achievements, friends, store listings, Workshop items, and current player counts. 14 tools across 5 categories, with a React dashboard and REST bridge.

---

## Features

- **Profile** — look up yourself, any player, friends list, resolve vanity URLs
- **Library** — owned games with playtime, recently played, detailed store info (no key needed)
- **Stats** — per-game achievements, global achievement percentages, current player counts, leaderboards
- **Store & News** — latest news per game, search the store by name
- **Workshop** — query published workshop items by app, sort by popularity/recency

No API key needed for: store details, player counts, news, achievement percentages, and store search. API key unlocks profile, library, friends, and Workshop.

---

## Quick Start

```powershell
# 1. Clone & install
git clone https://github.com/sandraschi/steam-mcp.git
cd steam-mcp
uv sync

# 2. Set your Steam Web API key (free)
#    Get one: https://steamcommunity.com/dev/apikey
$env:STEAM_API_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
$env:STEAM_ID = "7656119xxxxxxxxxx"   # your 64-bit Steam ID

# 3. Start the server
just serve
```

Server runs on `http://localhost:11020`. MCP endpoint at `http://localhost:11020/mcp`. REST bridge at `/api/status`, `/api/tools`, `/api/tools/{name}/call`.

---

## Tools

### Profile

| Tool | Description | Key |
|------|-------------|:----:|
| `get_own_profile` | Player summary for configured STEAM_ID | Yes |
| `get_player_summaries(steamids)` | Look up any player(s) by Steam ID | Yes |
| `get_friend_list(steamid)` | List friends for a user | Yes |
| `resolve_vanity_url(vanity_url)` | Resolve custom URL to 64-bit Steam ID | Yes |

### Library

| Tool | Description | Key |
|------|-------------|:----:|
| `get_owned_games(steamid)` | Full game library with playtime | Yes |
| `get_recently_played_games(steamid)` | Recently played games | Yes |
| `get_app_details(app_id)` | Store page data (name, price, description, screenshots) | No |

### Stats

| Tool | Description | Key |
|------|-------------|:----:|
| `get_player_achievements(steamid, app_id)` | Player's achievements for a game | Yes |
| `get_global_achievement_percentages(app_id)` | Global completion rates | No |
| `get_number_of_current_players(app_id)` | Concurrent players right now | No |
| `get_game_leaderboards(app_id)` | List leaderboards for a game | Yes |

### Store & News

| Tool | Description | Key |
|------|-------------|:----:|
| `get_news_for_app(app_id)` | Latest news articles | No |
| `search_store(query)` | Search games by name | No |

### Workshop

| Tool | Description | Key |
|------|-------------|:----:|
| `query_workshop_items(app_id, query)` | Query Workshop items | Yes |

---

## Usage

### As an MCP server (for AI assistants)

Connect any MCP-compatible client to the STDIO or HTTP endpoint:

```json
// Claude Desktop, opencode, etc.
{
  "mcpServers": {
    "steam": {
      "command": "uv",
      "args": ["run", "steam-mcp"],
      "env": {
        "STEAM_API_KEY": "...",
        "STEAM_ID": "..."
      }
    }
  }
}
```

Or via HTTP SSE:

```json
{
  "mcpServers": {
    "steam": {
      "url": "http://localhost:11020/mcp"
    }
  }
}
```

### Via REST API

```bash
# Status
curl http://localhost:11020/api/status

# List tools
curl http://localhost:11020/api/tools

# Call a tool
curl -X POST http://localhost:11020/api/tools/get_number_of_current_players/call \
  -H "Content-Type: application/json" \
  -d '{"arguments": {"app_id": 440}}'
```

### Via React Dashboard

```powershell
start.ps1         # launches backend + frontend
# or
just frontend-dev # frontend only on http://localhost:11021
```

---

## Godot + Steam Publishing

This MCP handles *accessing* Steam data. To *publish* a Godot game on Steam:

1. **GodotSteam** ([godotsteam.com](https://godotsteam.com)) — GDExtension that wraps Steamworks SDK as native Godot nodes. Handles achievements, leaderboards, lobbies, networking, Workshop, overlay, DRM, cloud saves.
2. **Steamworks Partner** — Register at [partner.steamgames.com](https://partner.steamgames.com). $100 Steam Direct fee per game, recoupable after $1K revenue. 70/30 revenue split.
3. **SteamPipe** — Upload builds via `steamcmd.exe`. Supports delta patching, beta branches, rollbacks.

---

## Architecture

```
src/steam_mcp/
  server.py          # FastAPI + MCP HTTP composition
  web.py             # REST bridge
  transport.py       # STDIO/HTTP transport
  config.py          # Env-based settings
  mcp/
    registry.py      # Shared FastMCP instance
    tools/           # Tool implementations (14 tools, 5 files)
      profile.py library.py stats.py store.py workshop.py
webapp/              # Vite React dashboard (TypeScript, Tailwind)
native/              # Tauri 2.0 scaffold (placeholder)
```

---

## Development

```powershell
uv sync                # Install Python deps
npm --prefix webapp i  # Install frontend deps
just serve             # Dev server with hot reload
just lint              # Ruff check
npm run build -w webapp    # Build frontend
```

---

## Ports

| Service | Port |
|---------|:----:|
| Backend (FastAPI + MCP HTTP) | 11020 |
| Frontend (Vite dev) | 11021 |
| MCP Streamable HTTP | `POST /mcp` on 11020 |

---

## License

MIT
