# Configuration

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `STEAM_API_KEY` | — | Steam Web API key from [steamcommunity.com/dev/apikey](https://steamcommunity.com/dev/apikey). Required for profile, library, workshop, and wishlist tools. |
| `STEAM_ID` | — | 64-bit Steam ID for default account queries. Find yours at [steamid.io](https://steamid.io/). |
| `BACKEND_PORT` | `11020` | Port for the FastAPI + MCP HTTP server |
| `FRONTEND_PORT` | `11021` | Port for the Vite React dev server |
| `HOST` | `127.0.0.1` | Bind address for the backend |
| `LOG_LEVEL` | `warning` | Logging level (debug, info, warning, error) |
| `STEAM_PREFAB_APPS` | `1` | Enable Prefab UI cards (`0` to disable for headless clients) |
| `STEAM_CHAT_MODE` | `hybrid` | Chat mode: `hybrid`, `llm`, or `rules` |
| `AI_PROVIDER` | `ollama` | LLM provider for AI chat (`ollama`, `openai`, `google`) |
| `AI_ENDPOINT` | `http://127.0.0.1:11434/v1/chat/completions` | LLM API endpoint |
| `AI_MODEL` | `llama3.1:8b` | LLM model name |
| `STEAMCMD_PATH` | — | Path to SteamCMD executable for publishing operations |
| `STEAM_APP_ID` | `0` | Steam App ID for publishing (Steamworks) |
| `STEAM_DEPOT_ID` | `0` | Steam Depot ID for publishing |
| `STEAM_USERNAME` | — | Steam partner login for steamcmd uploads |
| `STEAMCMD_PASSWORD` | — | Optional; omit for Steam Guard interactive login |
| `FLEET_EXCHANGE_ROOT` | — | Local path for staged build artifacts |
| `STEAM_MCP_URL` | — | Used by godot-mcp to find this server (default `http://127.0.0.1:11020`) |

## Setting Variables

In `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "steam": {
      "command": "uv",
      "args": ["--directory", "C:\\path\\to\\steam-mcp", "run", "steam-mcp"],
      "env": {
        "STEAM_API_KEY": "your-key",
        "STEAM_ID": "7656119xxxxxxxxxx",
        "STEAMCMD_PATH": "D:\\Tools\\steamcmd\\steamcmd.exe",
        "STEAM_CHAT_MODE": "hybrid"
      }
    }
  }
}
```

For shell sessions:

```powershell
$env:STEAM_API_KEY = "your-key"
$env:STEAM_ID = "7656119xxxxxxxxxx"
```
