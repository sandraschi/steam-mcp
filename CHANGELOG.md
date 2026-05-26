# Changelog

## 0.1.0 (2026-05-25)

- Initial release: 14 MCP tools across 5 categories
- Profile: get_own_profile, get_player_summaries, get_friend_list, resolve_vanity_url
- Library: get_owned_games, get_recently_played_games, get_app_details
- Stats: get_player_achievements, get_global_achievement_percentages, get_number_of_current_players, get_game_leaderboards
- Store: get_news_for_app, search_store
- Workshop: query_workshop_items
- FastAPI + FastMCP HTTP bridge on port 11020
- React dashboard (Vite + Tailwind) on port 11021
- REST bridge at /api/status, /api/tools, /api/tools/{name}/call
- Ports registered in fleet registry
