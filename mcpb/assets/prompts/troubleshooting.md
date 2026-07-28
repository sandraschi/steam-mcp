# Steam-MCP — Troubleshooting

## MCP client cannot connect (STDIO)

- Verify `uv sync` completed
- Test: `uv run python -m steam_mcp.server --stdio`
- Check client config uses `uv run --directory <repo> steam-mcp` or `install-mcp.ps1`

## HTTP MCP unreachable

- Start backend: `just serve` or `uv run python -m steam_mcp.server --http --port 11020`
- URL must be `http://127.0.0.1:11020/mcp` (not https unless you terminate TLS)
- Firewall: allow loopback 11020

## Well-known manifest 404

- Requires FastAPI app (`just serve`), not STDIO-only mode
- Path: `/.well-known/mcp/manifest.json`

## 401 / invalid key errors from Steam

- Regenerate key at steamcommunity.com/dev/apikey
- Key is tied to domain — use consistent hostname
- Some endpoints fail if profile is private and key doesn't match owner

## Rate limiting

Steam may throttle aggressive polling. Space out repeated `players` or `search` calls.

## PyInstaller / Tauri sidecar

- Build sidecar: `.\native\build-sidecar.ps1`
- Output: `native/binaries/steam-mcp-backend-x86_64-pc-windows-msvc.exe`
- Then: `cd native; npm run build`

## MCPB bundle rejected

- Run `just mcpb-pack` and ensure `manifest.json` + `src/` + `assets/` present
- Do not include `.venv`, `webapp/node_modules`, or `glama.json` (see `.mcpbignore`)

## Tests

```powershell
just test
just smoke
```
