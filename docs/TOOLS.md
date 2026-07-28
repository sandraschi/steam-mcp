# Tool Reference

## Portmanteau Tools

All tools follow the portmanteau pattern: one MCP tool with an `operation` parameter to select the action.

### `steam_profile`

Query Steam player profiles.

| Operation | Params | Auth | Description |
|-----------|--------|------|-------------|
| `own` | — | API key + Steam ID | Your configured profile |
| `summaries` | `steamids` (comma-separated) | API key | Any player summaries |
| `friends` | `steamid`, `relationship` | API key | Friend list |
| `resolve_vanity` | `vanity_url` | API key | Custom URL to Steam ID |

**Examples:**
```json
{"operation": "own"}
{"operation": "summaries", "steamids": "76561197960435530"}
{"operation": "friends", "steamid": "76561197960435530"}
{"operation": "resolve_vanity", "vanity_url": "sandraschi"}
```

### `steam_library`

Access game library data.

| Operation | Params | Auth | Description |
|-----------|--------|------|-------------|
| `owned` | `steamid`, `include_free` | API key | All owned games with playtime |
| `recent` | `steamid`, `count` | API key | Recently played games |
| `details` | `app_id`, `country` | None | Store details and pricing |
| `wishlist` | `steamid` | API key | Wishlist items |

**Examples:**
```json
{"operation": "owned"}
{"operation": "players", "app_id": 440}
{"operation": "details", "app_id": 440, "country": "DE"}
```

### `steam_stats`

Game statistics and player counts.

| Operation | Params | Auth | Description |
|-----------|--------|------|-------------|
| `achievements` | `steamid`, `app_id` | API key | Per-player achievements |
| `global_percentages` | `app_id` | None | Achievement rarity |
| `players` | `app_id` | None | Concurrent player count |
| `leaderboards` | `app_id` | API key | Leaderboard listing |

**Examples:**
```json
{"operation": "players", "app_id": 440}
{"operation": "global_percentages", "app_id": 730}
{"operation": "achievements", "steamid": "76561197960435530", "app_id": 440}
```

### `steam_store`

Browse the Steam store.

| Operation | Params | Auth | Description |
|-----------|--------|------|-------------|
| `news` | `app_id`, `count` | None | Latest app news |
| `search` | `query`, `count` | None | Find games by name |
| `reviews` | `app_id`, `count` | None | User reviews with scores |

**Examples:**
```json
{"operation": "search", "query": "Godot", "count": 5}
{"operation": "news", "app_id": 570, "count": 3}
{"operation": "reviews", "app_id": 730}
```

### `steam_workshop`

Browse Workshop content.

| Operation | Params | Auth | Description |
|-----------|--------|------|-------------|
| `query` | `app_id`, `query`, `count`, `sort_by` | API key | Search items |
| `item_details` | `published_file_ids` | API key | File metadata |

**Examples:**
```json
{"operation": "query", "app_id": 440, "sort_by": "mostsubscribed", "count": 10}
{"operation": "item_details", "published_file_ids": "12345,67890"}
```

### `steam_system`

Server health and tools.

| Operation | Params | Auth | Description |
|-----------|--------|------|-------------|
| `status` | — | None | Auth config + tool count |
| `steamcmd_status` | — | None | SteamCMD binary detection |

### `steam_publish`

Steamworks publishing pipeline.

| Operation | Params | Auth | Description |
|-----------|--------|------|-------------|
| `status` | — | None | Publishing config status |
| `checklist` | — | None | Readiness checklist |
| `monetization` | — | None | Monetization guide |
| `validate_build` | `build_dir` | None | Build directory validation |
| `generate_vdf` | `app_id`, `depot_id` | None | SteamPipe VDF generation |
| `upload_build` | `app_id`, `depot_id`, `build_dir`, `branch`, `dry_run` | None | Build upload (dry-run by default) |
| `upload_prerelease` | `app_id`, `depot_id`, `build_dir`, `branch`, `dry_run` | None | Prerelease upload |
| `upload_release` | `app_id`, `depot_id`, `build_dir`, `branch`, `dry_run` | None | Release upload to public branch |

All upload operations default to `dry_run=true`. Set `dry_run=false` to execute.

```powershell
# Check readiness
curl -X POST http://localhost:11020/api/tools/steam_publish/call `
  -H "Content-Type: application/json" `
  -d '{"arguments":{"operation":"checklist"}}'

# Preview VDF without uploading
curl -X POST http://localhost:11020/api/tools/steam_publish/call `
  -H "Content-Type: application/json" `
  -d '{"arguments":{"operation":"generate_vdf","app_id":1234560,"depot_id":1234561}}'
```

### Fleet Pipeline

In the fleet game pipeline, **godot-mcp** handles Windows export and staging, then calls steam-mcp for the upload:

| Step | Tool |
|------|------|
| Export Windows build | `godot-mcp`: `just little-game-export windows` |
| Stage to exchange | `godot-mcp`: `steam_stage_build` |
| Generate VDF + upload | steam-mcp: `steam_publish(operation='upload_build')` |
| Full pipeline | godot-mcp: `ship_to_steam` (automates all steps) |

Set `STEAM_MCP_URL` in godot-mcp to point to this server (default `http://127.0.0.1:11020`).

### `steam_help`

Multi-level help.

| Param | Description |
|-------|-------------|
| `level` | `brief`, `full`, or `operations` |

## Additional Tools

| Tool | Description |
|------|-------------|
| `agentic_steam_workflow` | Multi-step Steam queries via host LLM sampling (SEP-1577) |
| `show_steam_status_card` | Prefab UI card: auth and connectivity status |
| `show_library_card` | Prefab UI card: owned games summary |
| `show_store_search_card` | Prefab UI card: store search results |
| `show_workshop_card` | Prefab UI card: Workshop items |
| `show_player_count_card` | Prefab UI card: concurrent player count |

## Auth Summary

| Auth Needed | Tools |
|-------------|-------|
| No key | `steam_store` (search, news), `steam_stats` (players, global_percentages), `steam_system`, `steam_help`, `steam_publish` |
| API key + Steam ID | `steam_profile`, `steam_library`, `steam_stats` (achievements, leaderboards), `steam_workshop` |
