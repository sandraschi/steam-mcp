"""LLM-backed chat routing for the web dashboard (Ollama / OpenAI-compatible)."""

from __future__ import annotations

import json
import os
import re
from typing import Any

import httpx
from fastmcp import FastMCP

from .config import settings

_JSON_BLOCK = re.compile(r"\{[\s\S]*\}")


class SteamAIRouter:
    """Ask a local/cloud LLM to emit a portmanteau tool call, then execute it."""

    def __init__(self, mcp_app: FastMCP):
        self.mcp = mcp_app
        self.provider = settings.ai_provider
        self.endpoint = settings.ai_endpoint
        self.model = settings.ai_model

    _SYSTEM = (
        "You are Steam-MCP assistant. Reply with ONE JSON object only — no markdown fences.\n"
        "Schema: {\"tool\": \"steam_store\", \"arguments\": {\"operation\": \"search\", \"query\": \"Godot\"}}\n"
        "Tools and operations:\n"
        "- steam_profile: own, summaries, friends, resolve_vanity\n"
        "- steam_library: owned, recent, details, wishlist\n"
        "- steam_stats: achievements, global_percentages, players, leaderboards\n"
        "- steam_store: news, search, reviews\n"
        "- steam_workshop: query, item_details\n"
        "- steam_system: status, steamcmd_status\n"
        "- steam_help: level brief|full|operations\n"
        "Use steam_store/search without API key when possible."
    )

    async def route_query(self, query: str) -> str:
        raw = await self._llm(query)
        tool_call = self._parse_tool_call(raw)
        if not tool_call:
            return raw.strip() or "LLM did not return a valid tool call."
        tool, arguments = tool_call
        result = await self.mcp.call_tool(tool, arguments)
        content = result.content[0].text if result.content else str(result)
        try:
            parsed = json.loads(content)
            if isinstance(parsed, dict):
                return str(parsed.get("message") or parsed)
        except (json.JSONDecodeError, TypeError, AttributeError):
            pass
        return content

    async def _llm(self, query: str) -> str:
        endpoint = self.endpoint or "http://127.0.0.1:11434/v1/chat/completions"
        model = self.model or "llama3.1:8b"
        headers: dict[str, str] = {"Content-Type": "application/json"}
        api_key = os.getenv("OPENAI_API_KEY", "")
        if api_key and self.provider in ("openai", "google"):
            headers["Authorization"] = f"Bearer {api_key}"
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                r = await client.post(
                    endpoint,
                    headers=headers,
                    json={
                        "model": model,
                        "messages": [
                            {"role": "system", "content": self._SYSTEM},
                            {"role": "user", "content": query},
                        ],
                        "temperature": 0.2,
                    },
                )
                if r.status_code == 200:
                    return r.json()["choices"][0]["message"]["content"]
                return f"LLM error {r.status_code}: {r.text[:300]}"
            except httpx.ConnectError:
                return (
                    f"LLM not reachable at {endpoint}. "
                    "Start Ollama or set AI_ENDPOINT / STEAM_CHAT_MODE=rules."
                )
            except Exception as exc:
                return f"LLM error: {exc}"

    def _parse_tool_call(self, text: str) -> tuple[str, dict[str, Any]] | None:
        match = _JSON_BLOCK.search(text or "")
        if not match:
            return None
        try:
            data = json.loads(match.group(0))
        except json.JSONDecodeError:
            return None
        tool = data.get("tool")
        arguments = data.get("arguments") or {}
        if not isinstance(tool, str) or not isinstance(arguments, dict):
            return None
        return tool, arguments


async def ollama_available() -> bool:
    for host in ("http://127.0.0.1:11434", "http://localhost:11434"):
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                r = await client.get(f"{host}/api/tags")
                if r.status_code == 200:
                    return True
        except (httpx.ConnectError, httpx.TimeoutException, httpx.HTTPError):
            continue
    return False
