<p align="center">
  <img src="https://img.shields.io/badge/python-3.12+-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/fastmcp-3.2+-purple" alt="FastMCP">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
  <img src="https://img.shields.io/badge/version-0.3.2-blue" alt="Version">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Port_Backend-11020-blueviolet" alt="Backend Port">
  <img src="https://img.shields.io/badge/Port_Frontend-11021-blueviolet" alt="Frontend Port">
  <img src="https://img.shields.io/badge/MCP_HTTP-%2Fmcp-ff69b4" alt="MCP Path">
</p>

# Steam-MCP

FastMCP 3.2 portmanteau server for Valve Steam — profile, library, stats, store, Workshop, and Steamworks publishing. React dashboard with hybrid AI chat, Prefab UI cards, fleet discovery, and Tauri native shell.

## Quick Install

```powershell
git clone https://github.com/sandraschi/steam-mcp.git
cd steam-mcp
uv sync
$env:STEAM_API_KEY = "your-key"   # steamcommunity.com/dev/apikey
$env:STEAM_ID = "7656119xxxxxxxxxx"
just serve              # backend :11020
```

MCP HTTP: `http://localhost:11020/mcp` — add to Claude Desktop config:

```json
{
  "mcpServers": {
    "steam": {
      "command": "uv",
      "args": ["--directory", "path/to/steam-mcp", "run", "steam-mcp"],
      "env": { "STEAM_API_KEY": "...", "STEAM_ID": "..." }
    }
  }
}
```

Full install reference: [INSTALL.md](INSTALL.md) (also see [AGENT_INSTALL_REFERENCE.md](https://github.com/sandraschi/mcp-central-docs/blob/main/standards/AGENT_INSTALL_REFERENCE.md) in fleet standards).

## What You Can Do

- *"Search for Godot games on Steam"*
- *"How many players are in Team Fortress 2 right now?"*
- *"Show my game library with playtime"*
- *"What are the latest updates for Cyberpunk 2077?"*

## Documentation

| Doc | Contents |
|-----|----------|
| [Installation](INSTALL.md) | All install methods, prerequisites |
| [Configuration](docs/CONFIGURATION.md) | Environment variables, Steam auth |
| [Tool Reference](docs/TOOLS.md) | All portmanteau tools and operations |
| [Steam Publishing](https://github.com/sandraschi/mcp-central-docs/blob/main/docs/gamedev/STEAM_PUBLISHING.md) | Steamworks setup, Direct fee, credentials |
| [Development](docs/DEVELOPMENT.md) | Contributing, local setup, standards |
| [Troubleshooting](docs/TROUBLESHOOTING.md) | Common issues and fixes |
| [Fleet Project Page](https://github.com/sandraschi/mcp-central-docs/blob/main/projects/steam-mcp/README.md) | Central docs overview |

## Cross-Fleet Pipeline

Steam-MCP is the publishing backend for **godot-mcp** — the fleet's Godot game builder. Export Windows builds from Godot, stage them in the fleet exchange, and upload via SteamPipe:

```
godot-mcp (export + stage) → steam-mcp (VDF + steamcmd upload)
```

See [godot-mcp Ship to Steam](https://github.com/sandraschi/godot-mcp/blob/main/docs/ship-to-steam.md) and [STEAM_PUBLISHING.md](https://github.com/sandraschi/mcp-central-docs/blob/main/docs/gamedev/STEAM_PUBLISHING.md) in mcp-central-docs.

## Requirements

- Python 3.12+ and [uv](https://docs.astral.sh/uv/)
- Steam Web API key for profile/library/workshop tools
- SteamCMD for publishing operations (optional)

## License

MIT
