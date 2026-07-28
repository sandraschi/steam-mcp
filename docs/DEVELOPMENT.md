# Development Setup

## Tools Required

Install these before continuing:

```powershell
# Windows (winget)
winget install astral-sh.uv
winget install Git.Git
winget install OpenJS.NodeJS
winget install Casey.Just

# Verify
uv --version
git --version
node --version
just --version
```

## Setup

```powershell
git clone https://github.com/sandraschi/steam-mcp.git
cd steam-mcp
uv sync --extra dev --extra test
```

## Common Tasks

```powershell
just test      # pytest
just lint      # ruff
just smoke     # smoke test
just serve     # backend :11020 + /mcp
just mcpb-pack # build MCPB bundle
just e2e       # Playwright e2e tests (webapp)
```

## Code Standards

- **Python**: Ruff linting (line-length 120, see `pyproject.toml`)
- **TypeScript**: Biome formatting + linting (see `webapp/biome.json`)
- **Tool pattern**: Portmanteau — group related operations under one tool with an `operation` enum
- **Auth**: Public tools (no key) for store search, player counts; key-gated for profile/library/workshop

## Package Structure

```
src/steam_mcp/
  services/          # Steam Web API layer (shared httpx client)
  mcp/tools/         # Portmanteau tool definitions + prefab/agentic/help
  skills/steam-mcp/  # MCP skill for agent hosts
  server.py          # FastAPI + /mcp mount
  web.py             # REST bridge + endpoints
  activity_log.py    # Tool call logging
  chat.py            # Chat orchestrator (LLM + rules)
webapp/              # Vite + React dashboard
  src/pages/         # Chat, Dashboard, Settings, Help, Profile, Games
  src/components/    # Shared layout (Sidebar, Topbar, AppLayout)
native/              # Tauri 2 desktop shell
```

## Publishing New Versions

1. Update `__version__` in `src/steam_mcp/__init__.py`
2. Update `CHANGELOG.md`
3. Run `just test` and `just lint`
4. Tag with `v<version>` and push
5. GitHub Actions builds MCPB + native Windows Tauri artifacts
