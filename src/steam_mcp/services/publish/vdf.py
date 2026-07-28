"""Generate SteamPipe ContentBuilder VDF files."""

from __future__ import annotations

from pathlib import Path

from . import config


def write_depot_vdf(
    *,
    depot_id: int,
    content_root: Path,
    dest: Path,
    depot_path: str = ".",
) -> Path:
    content_root = content_root.resolve()
    lines = [
        '"DepotBuildConfig"',
        "{",
        f'\t"DepotID" "{depot_id}"',
        f'\t"ContentRoot" "{_vdf_path(content_root)}"',
        '\t"FileMapping"',
        "\t{",
        '\t\t"LocalPath" "*"',
        f'\t\t"DepotPath" "{depot_path}"',
        '\t\t"recursive" "1"',
        "\t}",
        "}",
        "",
    ]
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text("\n".join(lines), encoding="utf-8")
    return dest.resolve()


def write_app_build_vdf(
    *,
    app_id: int,
    depot_id: int,
    content_root: Path,
    build_output: Path,
    depot_vdf: Path,
    dest: Path,
    desc: str,
    set_live: str,
) -> Path:
    lines = [
        '"appbuild"',
        "{",
        f'\t"appid" "{app_id}"',
        f'\t"desc" "{desc}"',
        f'\t"buildoutput" "{_vdf_path(build_output.resolve())}"',
        f'\t"contentroot" "{_vdf_path(content_root.resolve())}"',
        f'\t"setlive" "{set_live}"',
        '\t"depots"',
        "\t{",
        f'\t\t"{depot_id}" "{_vdf_path(depot_vdf.resolve())}"',
        "\t}",
        "}",
        "",
    ]
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text("\n".join(lines), encoding="utf-8")
    return dest.resolve()


def generate_build_vdfs(
    *,
    app_id: int | None = None,
    depot_id: int | None = None,
    branch: str = "",
    desc: str = "",
    content_root_override: str = "",
) -> dict:
    aid = app_id or config.steam_app_id()
    did = depot_id or config.steam_depot_id()
    if not aid or not did:
        return {"success": False, "error": "STEAM_APP_ID and STEAM_DEPOT_ID required"}

    content = Path(content_root_override).resolve() if content_root_override else config.content_root(aid)
    if not content.is_dir():
        return {"success": False, "error": f"Content root missing: {content}"}

    scripts = config.scripts_root(aid)
    output = config.build_output_root(aid)
    scripts.mkdir(parents=True, exist_ok=True)
    output.mkdir(parents=True, exist_ok=True)

    branch_name = branch or config.steam_branch()
    build_desc = desc or f"Build {config.steam_build_id()} — {branch_name}"

    depot_vdf = scripts / f"depot_build_{did}.vdf"
    app_vdf = scripts / f"app_build_{aid}.vdf"

    write_depot_vdf(depot_id=did, content_root=content, dest=depot_vdf)
    write_app_build_vdf(
        app_id=aid,
        depot_id=did,
        content_root=content,
        build_output=output,
        depot_vdf=depot_vdf,
        dest=app_vdf,
        desc=build_desc,
        set_live=branch_name,
    )

    return {
        "success": True,
        "app_id": aid,
        "depot_id": did,
        "branch": branch_name,
        "content_root": str(content),
        "app_build_vdf": str(app_vdf),
        "depot_build_vdf": str(depot_vdf),
        "build_output": str(output),
    }


def _vdf_path(path: Path) -> str:
    return str(path).replace("/", "\\")
