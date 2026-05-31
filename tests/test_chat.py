from steam_mcp.chat_rules import _extract_app_id, _extract_query


def test_extract_app_id():
    assert _extract_app_id("players in app 570") == 570
    assert _extract_app_id("no id here", default=440) == 440


def test_extract_query():
    assert _extract_query('search for "Half-Life"') == "Half-Life"
    assert _extract_query("find portal games") == "portal games"
