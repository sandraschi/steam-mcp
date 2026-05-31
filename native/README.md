# Steam-MCP Native Shell (Tauri 2)

Desktop wrapper around the Vite dashboard and Python backend sidecar (port **11020**).

## Prerequisites

- Rust toolchain (`rustup`)
- Node.js 20+
- `uv` + Python 3.12
- Visual Studio Build Tools (Windows)

## Dev

```powershell
# Terminal 1 — backend
just serve

# Terminal 2 — Tauri + Vite (proxies /api → 11020)
cd native
npm install
npm run dev
```

## Release build

```powershell
.\native\build.ps1
```

Steps: webapp `npm run build` → PyInstaller sidecar → Tauri NSIS installer.

Sidecar only:

```powershell
.\native\build-sidecar.ps1
```

Reference: `email-mcp/native/` (same fleet pattern).
