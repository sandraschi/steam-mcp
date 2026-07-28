# Installing Steam-MCP

## Prerequisites

| Tool | Purpose | Install |
|------|---------|---------|
| [Python 3.12+](https://www.python.org/downloads/) | Run the server | `winget install Python.Python.3.12` |
| [uv](https://docs.astral.sh/uv/) | Python package manager | `winget install astral-sh.uv` |
| Git | Clone repo (Option B/C only) | `winget install Git.Git` |

## Option A — Manual (Recommended)

```powershell
git clone https://github.com/sandraschi/steam-mcp.git
cd steam-mcp
uv sync
```

Set environment variables (see [Configuration](docs/CONFIGURATION.md)) and start:

```powershell
just serve              # backend :11020 + MCP /mcp
.\start.ps1             # backend + frontend :11021
```

## Option B — MCP Client Config (Claude Desktop)

Add to your `claude_desktop_config.json`:

**STDIO (recommended):**
```json
{
  "mcpServers": {
    "steam": {
      "command": "uv",
      "args": ["--directory", "C:\\path\\to\\steam-mcp", "run", "steam-mcp"],
      "env": {
        "STEAM_API_KEY": "your-key",
        "STEAM_ID": "7656119xxxxxxxxxx"
      }
    }
  }
}
```

**HTTP (server must be running):**
```json
{
  "mcpServers": {
    "steam": { "url": "http://localhost:11020/mcp" }
  }
}
```

Config file location:
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

Restart Claude Desktop after adding.

## Option C — MCPB Bundle

Download `steam-mcp.mcpb` from the [Releases](https://github.com/sandraschi/steam-mcp/releases) page and drag it onto Claude Desktop, or:

```bash
npx @anthropic-ai/mcpb install https://github.com/sandraschi/steam-mcp
```

## Fleet Install Reference

For agent-based install flows across the fleet, see `mcp-central-docs/standards/AGENT_INSTALL_REFERENCE.md`.

## Verify Installation

Start the server and check the status endpoint:

```powershell
curl http://localhost:11020/api/status
```

Expected response includes `"status": "ok"` and a list of registered tools.

## Troubleshooting

See [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for common issues.
