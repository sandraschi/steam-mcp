"""Steamworks publishing portmanteau tool."""

from __future__ import annotations

from typing import Annotated, Any, Literal

from pydantic import Field

from ...services import publish
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
    operation: Annotated[PublishOp, Field(description="Steamworks publishing operation.")],
    content_root: Annotated[str, Field(description="Depot content folder (game files).", default="")] = "",
    branch: Annotated[str, Field(description="Steam branch: beta (prerelease) or default (live).", default="")] = "",
    desc: Annotated[str, Field(description="Build description for app_build VDF.", default="")] = "",
    app_build_vdf: Annotated[str, Field(description="Path to app_build VDF for upload_build.", default="")] = "",
    dry_run: Annotated[bool, Field(description="If true, upload_build only returns command without running steamcmd.", default=True)] = True,
) -> dict[str, Any]:
    """Steamworks partner publishing: checklist, VDF generation, SteamPipe upload.

    Requires STEAM_APP_ID, STEAM_DEPOT_ID, STEAM_USERNAME, STEAMCMD_PATH.
    Optional: STEAMCMD_PASSWORD, STEAM_CONTENT_ROOT, FLEET_EXCHANGE_ROOT.

    ## Operations
    - status — publish readiness summary
    - checklist — Steam Direct / release checklist
    - monetization — pricing and revenue guidance
    - validate_build — verify content folder
    - generate_vdf — write app_build + depot_build VDFs
    - upload_build — run steamcmd (dry_run default true)
    - upload_prerelease — generate VDF for beta branch + upload
    - upload_release — generate VDF for default branch + upload
    """
    if operation == "status":
        return await publish.publish_status()
    if operation == "checklist":
        return publish.publish_checklist(build_path=content_root, branch=branch)
    if operation == "monetization":
        return publish.monetization_guide()
    if operation == "validate_build":
        return await publish.validate_build(content_root)
    if operation == "generate_vdf":
        return await publish.generate_vdf(branch=branch, desc=desc, content_root=content_root)
    if operation == "upload_build":
        return await publish.upload_build(app_build_vdf, dry_run=dry_run)
    if operation == "upload_prerelease":
        return await publish.upload_prerelease(content_root, dry_run=dry_run)
    if operation == "upload_release":
        return await publish.upload_release(content_root, dry_run=dry_run)
    return {"success": False, "message": f"Unknown operation: {operation}", "data": None}
