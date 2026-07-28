"""Shared HTTP client for Steam API calls."""

from __future__ import annotations

import httpx

from . import __version__

_client: httpx.AsyncClient | None = None


async def init_client() -> None:
    global _client
    if _client is None:
        _client = httpx.AsyncClient(
            timeout=30.0,
            headers={"User-Agent": f"steam-mcp/{__version__}"},
            follow_redirects=True,
        )


async def close_client() -> None:
    global _client
    if _client is not None:
        await _client.aclose()
        _client = None


def get_client() -> httpx.AsyncClient:
    if _client is None:
        raise RuntimeError("HTTP client not initialized — server lifespan did not run")
    return _client
