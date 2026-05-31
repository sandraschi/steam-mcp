default:
    @just --list

run:
    uv run python -m steam_mcp.server

run-http:
    uv run python -m steam_mcp.server --http --port 11020

serve:
    uv run uvicorn steam_mcp.server:app --host 127.0.0.1 --port 11020 --reload

install:
    uv sync --extra dev --extra test

lint:
    uv run ruff check src/ tests/

fmt:
    uv run ruff format src/ tests/

test:
    uv run pytest tests/ -q

smoke:
    uv run python scripts/smoke_test.py

mcpb-pack:
    uv run python build_mcpb.py

llms-full:
    uv run python scripts/generate_llms_full.py

install-mcp CLIENT="print":
    pwsh -NoLogo -File install-mcp.ps1 {{CLIENT}}

frontend-install:
    cd webapp; npm install

frontend-dev:
    cd webapp; npx vite --port 11021 --host

frontend-build:
    cd webapp; npm run build

native-sidecar:
    pwsh -NoLogo -File native/build-sidecar.ps1

native-build:
    pwsh -NoLogo -File native/build.ps1

native-dev:
    cd native; npm install; npm run dev

e2e:
    cd webapp; npx playwright test

ports:
    @echo "Backend:  11020"
    @echo "Frontend: 11021"
    @echo "MCP HTTP: 11020/mcp"
