default:
    @just --list

# === Steam-MCP Justfile ===

# Run MCP server via STDIO (for MCP client)
run:
    uv run python -m steam_mcp.server

# Run MCP server via HTTP SSE on backend port
run-http:
    uv run python -m steam_mcp.server --http --port 11020

# Run REST API server (FastAPI + MCP at /mcp)
serve:
    uv run uvicorn steam_mcp.server:app --host 127.0.0.1 --port 11020 --reload

# Install Python deps
install:
    uv sync

# Lint Python code
lint:
    uv run ruff check src/ steam_mcp/

# Format Python code
format:
    uv run ruff format src/ steam_mcp/

# Install frontend deps
frontend-install:
    cd webapp && npm install

# Run frontend dev server
frontend-dev:
    cd webapp && npx vite --port 11021 --host

# Build frontend for production
frontend-build:
    cd webapp && npm run build

# Run e2e tests
e2e:
    cd webapp && npx playwright test

# Show ports
ports:
    @echo "Backend:  11020"
    @echo "Frontend: 11021"
    @echo "MCP HTTP: 11020/mcp"
