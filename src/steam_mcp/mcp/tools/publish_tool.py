"""steam_publish portmanteau tool for Steamworks publishing."""

from __future__ import annotations

from typing import Annotated, Any, Literal

from pydantic import Field

from ...services.publish import (
    generate_vdf,
    monetization_guide,
    publish_checklist,
    publish_status,
    upload_build,
    upload_prerelease,
    upload_release,
    validate_build,
)
from ..registry import TOOL_VERSION, mcp

PublishOp = Literal[
    "status",
    "checklist",
    "monetization",
    "validate_build",
    "generate_vdf",
    "upload_build",
    "upload_prerelease",
    "upload_release",
]


@mcp.tool(version=TOOL_VERSION)
async def steam_publish(
    operation: Annotated[PublishOp, Field(description="Publishing operation to run.")],
    app_id: Annotated[int, Field(description="Steam App ID for publishing operations.")] = 0,
    depot_id: Annotated[int, Field(description="Steam Depot ID for upload operations.")] = 0,
    build_dir: Annotated[str, Field(description="Path to build directory for upload.")] = "",
    dry_run: Annotated[bool, Field(description="Preview without uploading.")] = True,
    branch: Annotated[str, Field(description="Steam branch for upload (e.g. beta, public).")] = "beta",
) -> dict[str, Any]:
    """Steamworks publishing pipeline: status checks, VDF generation, and SteamPipe upload orchestration."""
    if operation == "status":
        return await publish_status()
    if operation == "checklist":
        return await publish_checklist()
    if operation == "monetization":
        return await monetization_guide()
    if operation == "validate_build":
        return await validate_build(build_dir)
    if operation == "generate_vdf":
        return await generate_vdf(app_id, depot_id)
    if operation == "upload_build":
        return await upload_build(app_id, depot_id, build_dir, branch, dry_run)
    if operation == "upload_prerelease":
        return await upload_prerelease(app_id, depot_id, build_dir, branch, dry_run)
    if operation == "upload_release":
        return await upload_release(app_id, depot_id, build_dir, branch, dry_run)
    return {"success": False, "message": f"Unknown operation: {operation}", "data": None}
