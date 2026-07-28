"""Steam release checklist (Steam Direct / Steamworks)."""

from __future__ import annotations

from typing import Any

from . import config


def publish_checklist(*, build_path: str = "", branch: str = "") -> dict[str, Any]:
    """Return partner publishing checklist with env/build readiness flags."""
    app_id = config.steam_app_id()
    depot_id = config.steam_depot_id()
    username = config.steam_username()
    steamcmd = config.steamcmd_path()
    branch_name = branch or config.steam_branch()

    content = config.content_root(app_id or None)
    build_ok = bool(build_path) and __import__("pathlib").Path(build_path).is_dir()

    items = [
        {
            "id": "steamworks_account",
            "label": "Steamworks partner account + Steam Direct fee paid",
            "required": True,
            "automated": False,
            "done": False,
            "hint": "https://partner.steamgames.com — $100 USD per app (recoupable)",
        },
        {
            "id": "app_id",
            "label": "App ID configured (STEAM_APP_ID)",
            "required": True,
            "automated": True,
            "done": app_id > 0,
            "value": app_id or None,
        },
        {
            "id": "depot_id",
            "label": "Depot ID configured (STEAM_DEPOT_ID)",
            "required": True,
            "automated": True,
            "done": depot_id > 0,
            "value": depot_id or None,
        },
        {
            "id": "store_page",
            "label": "Store page: capsules, screenshots, description, tags",
            "required": True,
            "automated": False,
            "done": False,
            "hint": "Can stay Coming Soon until build is ready",
        },
        {
            "id": "content_survey",
            "label": "Content survey / age rating answered",
            "required": True,
            "automated": False,
            "done": False,
        },
        {
            "id": "windows_build",
            "label": "Windows x64 build staged for depot",
            "required": True,
            "automated": True,
            "done": build_ok,
            "path": build_path or str(content),
        },
        {
            "id": "steamcmd",
            "label": "SteamCMD installed (STEAMCMD_PATH)",
            "required": True,
            "automated": True,
            "done": bool(steamcmd) and __import__("pathlib").Path(steamcmd).is_file(),
            "path": steamcmd or None,
        },
        {
            "id": "partner_login",
            "label": "Partner account for upload (STEAM_USERNAME)",
            "required": True,
            "automated": True,
            "done": bool(username),
        },
        {
            "id": "pricing",
            "label": "Price set in Steamworks (free OK)",
            "required": True,
            "automated": False,
            "done": False,
            "hint": "Monetization: set base price, regional pricing, discounts in partner dashboard",
        },
        {
            "id": "branch",
            "label": f"Target branch: {branch_name}",
            "required": True,
            "automated": True,
            "done": True,
            "hint": "beta = prerelease testing; default = live release branch",
        },
    ]

    required = [i for i in items if i["required"]]
    done_auto = sum(1 for i in required if i["done"])
    return {
        "success": True,
        "branch": branch_name,
        "items": items,
        "summary": f"{done_auto}/{len(required)} automated checks passing",
        "ready_for_upload": all(
            i["done"] for i in items if i["id"] in {"app_id", "depot_id", "windows_build", "steamcmd", "partner_login"}
        ),
        "ready_for_release": False,
        "monetization_note": "Revenue share ~70/30. Refunds handled by Valve. Set price before switching Coming Soon → Released.",
        "docs": "mcp-central-docs/docs/gamedev/STEAM_PUBLISHING.md",
    }


def monetization_guide() -> dict[str, Any]:
    return {
        "success": True,
        "topics": [
            {"id": "steam_direct", "fee": "$100 USD per app", "recoup": "After $1,000 gross on that app"},
            {"id": "revenue_share", "developer": "70%", "valve": "30%", "note": "Confirm current tier on Steamworks"},
            {"id": "free_game", "allowed": True, "note": "Set base price $0.00 in Steamworks"},
            {"id": "dlc", "note": "Create separate App IDs / depots for DLC in Steamworks"},
            {"id": "bundles", "note": "Package deals configured in Steamworks Packages"},
            {"id": "sales", "note": "Steam seasonal sales — opt in via partner dashboard"},
        ],
        "prerelease_flow": "Coming Soon store page + upload to beta branch + internal playtest keys",
        "release_flow": "Complete checklist → set live on default branch → Valve review → Released",
    }
