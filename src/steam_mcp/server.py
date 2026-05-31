from contextlib import asynccontextmanager
from pathlib import Path

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import __version__
from .client import close_client, init_client
from .config import settings
from .mcp import tools as _tools  # noqa: F401 — triggers @mcp.tool registration
from .mcp.registry import mcp
from .web import setup_webapp

logger = structlog.get_logger("steam-mcp")


def _register_skills_provider() -> None:
    try:
        from fastmcp.server.providers.skills import SkillsDirectoryProvider
    except ImportError:
        return
    roots = Path(__file__).resolve().parent / "skills"
    if not roots.is_dir():
        return
    try:
        mcp.add_provider(SkillsDirectoryProvider(roots=roots))
    except (OSError, UnicodeError, ValueError) as exc:
        logger.warning("skills_provider_skipped", error=str(exc))


_register_skills_provider()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_client()
    logger.info("steam_mcp_started", port=settings.backend_port, version=__version__)
    yield
    await close_client()
    logger.info("steam_mcp_stopped")


_mcp_asgi = mcp.http_app(path="/")

app = FastAPI(title="Steam-MCP", version=__version__, lifespan=lifespan)
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
