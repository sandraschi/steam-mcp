# Steam-MCP Native Shell (Tauri 2) — Scaffold

Planned desktop wrapper around the Vite dashboard and Python backend sidecar.

## Status

**Deferred** — use `start.ps1` or `webapp/start.ps1` for now.

## Target layout

```
native/
  src-tauri/     # Tauri 2 app
  package.json   # tauri CLI scripts
  build.ps1      # sidecar + bundle
```

## Build prerequisites (future)

- Rust toolchain
- Node.js 20+
- Built backend sidecar (`uv run pyinstaller` or fleet standard)

See `email-mcp/native/` for reference implementation.
