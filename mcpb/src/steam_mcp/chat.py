"""Lightweight chat orchestrator for the webapp — rules + optional Ollama LLM."""

from __future__ import annotations

from .ai import SteamAIRouter, ollama_available
from .chat_rules import handle_rule_query
from .config import settings
from .mcp.registry import mcp

_router: SteamAIRouter | None = None


def get_ai_router() -> SteamAIRouter:
    global _router
    if _router is None:
        _router = SteamAIRouter(mcp)
    return _router


async def handle_chat_query(query: str) -> dict[str, str]:
    mode = settings.chat_mode
    if mode in ("llm", "hybrid"):
        if mode == "llm" or await ollama_available():
            text = await get_ai_router().route_query(query)
            if not text.startswith("LLM not reachable"):
                return {"response": text, "mode": "llm"}
    return await handle_rule_query(query)
