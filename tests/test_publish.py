"""Tests for Steamworks publish helpers."""

from __future__ import annotations

from pathlib import Path

from steam_mcp.services.publish import checklist, vdf


def test_publish_checklist_missing_env(monkeypatch):
    monkeypatch.delenv("STEAM_APP_ID", raising=False)
    monkeypatch.delenv("STEAM_DEPOT_ID", raising=False)
    result = checklist.publish_checklist()
    assert result["success"] is True
    assert result["ready_for_upload"] is False


def test_generate_vdf_writes_files(tmp_path, monkeypatch):
    monkeypatch.setenv("STEAM_APP_ID", "480")
    monkeypatch.setenv("STEAM_DEPOT_ID", "481")
    monkeypatch.setenv("FLEET_EXCHANGE_ROOT", str(tmp_path))
    content = tmp_path / "steam-builds" / "480" / "content"
    content.mkdir(parents=True)
    (content / "game.exe").write_bytes(b"exe")

    result = vdf.generate_build_vdfs(branch="beta", desc="test build")
    assert result["success"] is True
    assert Path(result["app_build_vdf"]).is_file()
    assert Path(result["depot_build_vdf"]).is_file()
    text = Path(result["app_build_vdf"]).read_text(encoding="utf-8")
    assert '"appid" "480"' in text
    assert '"setlive" "beta"' in text


def test_monetization_guide():
    guide = checklist.monetization_guide()
    assert guide["success"] is True
    assert any(t["id"] == "revenue_share" for t in guide["topics"])
