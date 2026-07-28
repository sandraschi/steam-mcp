"""Steamworks publish orchestration."""

from __future__ import annotations

from pathlib import Path

from . import checklist, config, steamcmd_runner, vdf


async def publish_status() -> dict:
    chk = checklist.publish_checklist()
    cmd = await steamcmd_runner.steamcmd_status()
    return {
        "success": True,
        "app_id": config.steam_app_id(),
        "depot_id": config.steam_depot_id(),
        "branch": config.steam_branch(),
        "content_root": str(config.content_root()),
        "steamcmd": cmd.get("data", {}),
        "checklist_summary": chk.get("summary"),
        "ready_for_upload": chk.get("ready_for_upload"),
    }


async def validate_build(content_root: str = "") -> dict:
    root = Path(content_root) if content_root else config.content_root()
    data = steamcmd_runner.validate_content(root)
    if not data.get("success"):
        return data
    chk = checklist.publish_checklist(build_path=str(root))
    data["checklist"] = chk
    return data


async def generate_vdf(
    branch: str = "",
    desc: str = "",
    content_root: str = "",
) -> dict:
    return vdf.generate_build_vdfs(branch=branch, desc=desc, content_root_override=content_root)


async def upload_build(
    app_build_vdf: str = "",
    dry_run: bool = True,
) -> dict:
    if not app_build_vdf:
        gen = vdf.generate_build_vdfs()
        if not gen.get("success"):
            return gen
        app_build_vdf = gen["app_build_vdf"]
    return steamcmd_runner.run_app_build(app_build_vdf, dry_run=dry_run)


async def upload_prerelease(content_root: str = "", dry_run: bool = True) -> dict:
    gen = await generate_vdf(branch="beta", content_root=content_root)
    if not gen.get("success"):
        return gen
    upload = await upload_build(gen["app_build_vdf"], dry_run=dry_run)
    return {"success": upload.get("success", False), "phase": "prerelease", "vdf": gen, "upload": upload}


async def upload_release(content_root: str = "", dry_run: bool = True) -> dict:
    gen = await generate_vdf(branch="default", content_root=content_root)
    if not gen.get("success"):
        return gen
    upload = await upload_build(gen["app_build_vdf"], dry_run=dry_run)
    chk = checklist.publish_checklist(build_path=content_root or str(config.content_root()))
    return {
        "success": upload.get("success", False),
        "phase": "release",
        "vdf": gen,
        "upload": upload,
        "checklist": chk,
        "release_note": "Complete manual Steamworks checklist before setlive=default in production.",
    }
