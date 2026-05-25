from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .mcp import tools as _tools  # noqa: F401 — triggers @mcp.tool registration
from .mcp.registry import mcp
from .web import setup_webapp


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


_mcp_asgi = mcp.http_app(path="/")

app = FastAPI(title="Steam-MCP", version="0.1.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
setup_webapp(app)
app.mount("/mcp", _mcp_asgi)


def main():
    import sys

    if "--http" in sys.argv or "--port" in sys.argv or len(sys.argv) > 1:
        from .transport import run_server

        run_server(mcp, "steam-mcp")
    else:
        print("Starting Steam-MCP via STDIO...", file=sys.stderr)
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
