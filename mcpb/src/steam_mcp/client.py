"""Shared HTTP client for Steam API calls."""

from __future__ import annotations

import httpx

_client: httpx.AsyncClient | None = None


async def init_client() -> None:
    global _client
    if _client is None:
        _client = httpx.AsyncClient(
            timeout=30.0,
            headers={"User-Agent": "steam-mcp/0.2.0"},
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
