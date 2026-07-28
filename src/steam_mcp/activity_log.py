"""Activity log for MCP tool calls via the REST bridge."""

from __future__ import annotations

from datetime import UTC, datetime

from fastapi import APIRouter


class ActivityLog:
    """In-memory log of tool call activity."""

    def __init__(self) -> None:
        self._entries: list[dict] = []

    def add(self, tool: str, arguments: dict, success: bool) -> None:
        self._entries.append(
            {
                "tool": tool,
                "arguments": arguments,
                "success": success,
                "timestamp": datetime.now(UTC).isoformat(),
            }
        )

    def recent(self, limit: int = 20) -> list[dict]:
        return self._entries[-limit:]


def create_log_router(log: ActivityLog) -> APIRouter:
    router = APIRouter()

    @router.get("/logs")
    async def get_logs(limit: int = 20):
        return {"entries": log.recent(limit)}

    return router
