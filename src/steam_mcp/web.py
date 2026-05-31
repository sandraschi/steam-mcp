from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import httpx
from fastapi import FastAPI
from fastapi.responses import JSONResponse, PlainTextResponse

from . import __version__
from .ai import ollama_available
from .chat import get_ai_router, handle_chat_query
from .config import settings
from .mcp.registry import mcp


def setup_webapp(app: FastAPI) -> None:
    ai_router = get_ai_router()

    @app.get("/health")
    async def health():
        return {"status": "ok", "version": __version__}

    @app.get("/api/status")
    async def api_status():
        tools = await mcp.list_tools()
        tool_names = [t.name for t in tools]
        llm_up = await ollama_available()
        return {
            "status": "ok",
            "version": __version__,
            "has_api_key": settings.has_api_key,
            "has_steam_id": settings.has_steam_id,
            "tool_count": len(tools),
            "tools": tool_names,
            "chat_mode": settings.chat_mode,
            "llm_available": llm_up,
            "capabilities": {
                "prefab": settings.prefab_apps and any(n.startswith("show_") for n in tool_names),
                "agentic": "agentic_steam_workflow" in tool_names,
                "prompts": True,
                "resources": True,
                "skills": True,
                "llm_chat": llm_up or settings.chat_mode == "rules",
            },
        }

    @app.get("/api/tools")
    async def api_tools():
        tools = await mcp.list_tools()
        return {
            "tools": [
                {
                    "name": t.name,
                    "description": t.description or "",
                    "inputSchema": t.parameters,
                }
                for t in tools
            ]
        }

    @app.get("/api/tools/{name}")
    async def api_tool_get(name: str):
        tool = await mcp.get_tool(name)
        if not tool:
            return JSONResponse({"success": False, "message": f"Tool '{name}' not found"}, status_code=404)
        return {
            "success": True,
            "data": {
                "name": tool.name,
                "description": tool.description or "",
                "inputSchema": tool.parameters,
            },
        }

    @app.post("/api/tools/{name}/call")
    async def api_tool_execute(name: str, body: dict):
        try:
            result = await mcp.call_tool(name, body.get("arguments", {}))
            content = result.content if hasattr(result, "content") else result
            if isinstance(content, list) and len(content) > 0:
                text = content[0].text if hasattr(content[0], "text") else str(content[0])
                try:
                    parsed = json.loads(text)
                    return {"success": True, "data": parsed}
                except (json.JSONDecodeError, TypeError):
                    return {"success": True, "data": text}
            return {"success": True, "data": content}
        except Exception as e:
            return JSONResponse({"success": False, "message": str(e)}, status_code=500)

    @app.get("/api/skills/{skill_id}")
    async def api_skill(skill_id: str):
        skill_path = Path(__file__).resolve().parent / "skills" / skill_id / "SKILL.md"
        if not skill_path.is_file():
            return JSONResponse({"success": False, "message": "Skill not found"}, status_code=404)
        return {"success": True, "content": skill_path.read_text(encoding="utf-8")}

    @app.post("/api/chat")
    async def api_chat(body: dict):
        """Natural-language chat routed to portmanteau tools."""
        query = (body.get("query") or "").strip()
        if body.get("tool"):
            result = await mcp.call_tool(body["tool"], body.get("arguments") or {})
            content = result.content[0].text if result.content else str(result)
            try:
                parsed = json.loads(content)
                message = parsed.get("message") or json.dumps(parsed, indent=2)
            except (json.JSONDecodeError, TypeError, AttributeError):
                message = content
            return {"response": message}
        return await handle_chat_query(query)

    @app.get("/api/llm/models")
    async def get_llm_models():
        providers: list[dict[str, Any]] = []
        async with httpx.AsyncClient(timeout=3.0) as client:
            ollama_ok = False
            for host in ("http://127.0.0.1:11434", "http://localhost:11434"):
                try:
                    r = await client.get(f"{host}/api/tags")
                    if r.status_code == 200:
                        models = [m["name"] for m in r.json().get("models", [])]
                        providers.append(
                            {
                                "id": "ollama",
                                "name": "Ollama",
                                "endpoint": f"{host}/v1/chat/completions",
                                "available": True,
                                "models": models,
                            }
                        )
                        ollama_ok = True
                        break
                except (httpx.ConnectError, httpx.TimeoutException, httpx.HTTPError):
                    continue
            if not ollama_ok:
                providers.append(
                    {
                        "id": "ollama",
                        "name": "Ollama",
                        "endpoint": "http://127.0.0.1:11434/v1/chat/completions",
                        "available": False,
                        "models": [],
                    }
                )
        return {
            "providers": providers,
            "active": {
                "provider": ai_router.provider,
                "endpoint": ai_router.endpoint,
                "model": ai_router.model,
                "chat_mode": settings.chat_mode,
            },
        }

    @app.post("/api/llm/configure")
    async def configure_llm(body: dict):
        if "provider" in body:
            ai_router.provider = str(body["provider"])
            settings.ai_provider = ai_router.provider
        if "endpoint" in body:
            ai_router.endpoint = str(body["endpoint"])
            settings.ai_endpoint = ai_router.endpoint
        if "model" in body:
            ai_router.model = str(body["model"])
            settings.ai_model = ai_router.model
        if "chat_mode" in body:
            settings.chat_mode = str(body["chat_mode"]).lower()
        return {"success": True, "active": {"provider": ai_router.provider, "model": ai_router.model}}

    @app.get("/resource://steam/capabilities")
    async def resource_capabilities():
        return PlainTextResponse(
            "# Steam-MCP\n\nPortmanteau tools on ports 11020/11021.\n",
            media_type="text/plain",
        )
