from __future__ import annotations

import json
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import JSONResponse, PlainTextResponse

from .chat import handle_chat_query
from .config import settings
from .mcp.registry import mcp


def setup_webapp(app: FastAPI) -> None:
    @app.get("/health")
    async def health():
        return {"status": "ok"}

    @app.get("/api/status")
    async def api_status():
        tools = await mcp.list_tools()
        tool_names = [t.name for t in tools]
        return {
            "status": "ok",
            "version": "0.2.1",
            "has_api_key": settings.has_api_key,
            "has_steam_id": settings.has_steam_id,
            "tool_count": len(tools),
            "tools": tool_names,
            "capabilities": {
                "prefab": any(n.startswith("show_") for n in tool_names),
                "agentic": "agentic_steam_workflow" in tool_names,
                "prompts": True,
                "resources": True,
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

    @app.get("/resource://steam/capabilities")
    async def resource_capabilities():
        return PlainTextResponse(
            "# Steam-MCP\n\nPortmanteau tools on ports 11020/11021.\n",
            media_type="text/plain",
        )
