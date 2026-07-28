# Troubleshooting

## Server won't start — ModuleNotFoundError

**Cause**: Missing runtime dependencies.  
**Fix**: Run `uv sync --extra dev --extra test` and verify the virtual environment is active.

## Tool returns API error

**Cause**: Steam Web API returns a non-200 status.  
**Fix**: Check `STEAM_API_KEY` is valid and hasn't been revoked. Some endpoints require both key and Steam ID.

## "STEAM_API_KEY not configured"

**Cause**: The environment variable is not set or empty.  
**Fix**: Set `$env:STEAM_API_KEY = "your-key"` (PowerShell) or add it to `claude_desktop_config.json` env block.

## "STEAM_ID not configured"

**Cause**: No Steam ID provided and `STEAM_ID` env var is empty.  
**Fix**: Set `$env:STEAM_ID = "7656119xxxxxxxxxx"` or pass `steamid` parameter to the tool call.

## Store search returns no results

**Cause**: Steam's SearchApps endpoint is case-sensitive or the query has no matches.  
**Fix**: Try different search terms. Verify at store.steampowered.com that the game exists.

## Webapp shows blank page

**Cause**: Backend not running or CORS misconfiguration.  
**Fix**: Ensure `just serve` is running on port 11020. Check the browser console for CORS errors.

## Prefab cards not showing

**Cause**: `STEAM_PREFAB_APPS` is set to `0` or `prefab-ui` is not installed.  
**Fix**: Set `$env:STEAM_PREFAB_APPS = "1"` and run `uv sync` to install prefab-ui dependency.

## LLM chat not available

**Cause**: Ollama not running or `AI_ENDPOINT` is misconfigured.  
**Fix**: Start Ollama (`ollama serve`), or set `STEAM_CHAT_MODE=rules` for rule-based offline chat.

## SteamCMD not detected

**Cause**: `STEAMCMD_PATH` is not set or points to a missing file.  
**Fix**: Install SteamCMD from [developer.valvesoftware.com](https://developer.valvesoftware.com/wiki/SteamCMD) and set the path to `steamcmd.exe`.

## "FastMCP server support is not installed"

**Cause**: `fastmcp` extra dependencies are missing.  
**Fix**: Run `uv sync` to ensure all dependencies including `fastmcp[server]` are installed.

## Command not found: `just`

**Cause**: Just command runner not installed.  
**Fix**: `winget install Casey.Just`
