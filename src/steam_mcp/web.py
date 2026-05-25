from fastapi import FastAPI
from fastapi.responses import JSONResponse

from .config import settings
from .mcp.registry import mcp


def setup_webapp(app: FastAPI) -> None:
    @app.get("/api/status")
    async def api_status():
        return {
            "status": "ok",
            "version": "0.1.0",
            "has_api_key": settings.has_api_key,
            "has_steam_id": settings.has_steam_id,
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
                import json

                text = content[0].text if hasattr(content[0], "text") else str(content[0])
                try:
                    parsed = json.loads(text)
                    return {"success": True, "data": parsed}
                except (json.JSONDecodeError, TypeError):
                    return {"success": True, "data": text}
            return {"success": True, "data": content}
        except Exception as e:
            return JSONResponse({"success": False, "message": str(e)}, status_code=500)
