# Steam-MCP Agent Skill

## Overview

Steam-MCP exposes Valve Steam data through FastMCP 3.2 portmanteau tools on ports **11020** (backend) and **11021** (frontend).

## Auth

- `STEAM_API_KEY` — required for profile, library, friends, workshop, wishlist
- `STEAM_ID` — your 64-bit Steam ID for `steam_profile(operation='own')` and default library queries
- Public endpoints: store search, app details, news, player counts, global achievement percentages

## Portmanteau Tools

| Tool | Operations |
|------|------------|
| `steam_profile` | own, summaries, friends, resolve_vanity |
| `steam_library` | owned, recent, details, wishlist |
| `steam_stats` | achievements, global_percentages, players, leaderboards |
| `steam_store` | news, search, reviews |
| `steam_workshop` | query, item_details |
| `steam_system` | status, steamcmd_status |

## Workflow Examples

- "What's in my library?" → `steam_library(operation='owned')`
- "How many people play TF2?" → `steam_stats(operation='players', app_id=440)`
- "Search for Godot games" → `steam_store(operation='search', query='Godot')`
- "Workshop mods for game X" → `steam_workshop(operation='query', app_id=…)`

## Agentic

Use `agentic_steam_workflow(goal='…')` when the host supports MCP sampling (SEP-1577).

## Prefab

- `show_steam_status_card` — auth/connectivity
- `show_library_card` — owned games
- `show_store_search_card` — store search results

## Publishing

For Godot/Steam publishing see `mcp-central-docs/docs/gamedev/STEAM_PUBLISHING.md`. Set `STEAMCMD_PATH` for `steam_system(operation='steamcmd_status')`.
