# Steam-MCP — User Guide & Tutorials

This document teaches end users and AI agents how to accomplish common Steam tasks through steam-mcp. Every tutorial includes the tool, required arguments, expected output, and troubleshooting tips.

## Installation

### Claude Desktop (MCPB)

1. Build or download `dist/steam-mcp.mcpb`
2. Drag the `.mcpb` file into Claude Desktop settings
3. Configure `STEAM_API_KEY` and `STEAM_ID` in the bundle user settings

### Cursor / VS Code / CLI

```powershell
cd D:\Dev\repos\steam-mcp
uv sync
.\install-mcp.ps1 cursor   # or claude, print, windsurf, zed
```

Set environment variables before starting the client:
```powershell
$env:STEAM_API_KEY = "your-key"
$env:STEAM_ID = "7656119xxxxxxxxxx"
```

### HTTP MCP (LobeHub / remote clients)

Point the client at:
```
http://127.0.0.1:11020/mcp
```

Discovery manifest:
```
http://127.0.0.1:11020/.well-known/mcp/manifest.json
```

---

## Tutorial 1: Search the Steam Store (No API Key)

**Goal:** Find games matching a keyword without any API key.

**Tool:** `steam_store`

**Arguments:**
```json
{"operation": "search", "query": "Godot", "count": 8}
```

**Expected output:**
```json
{
  "success": true,
  "message": "Found N results for 'Godot': ...",
  "data": {
    "results": [
      {"appid": 12345, "name": "Godot Engine", "tiny_image": "https://...", "metascore": "85"},
      {"appid": 67890, "name": "Godot Game", "tiny_image": "https://..."}
    ]
  }
}
```

**Prefab alternative:** `show_store_search_card(query="Godot")` — renders a visual card.

**How it works:** The Steam store search API returns games, DLC, software, and videos matching the query. Results include app ID, name, thumbnail, and optionally price, platform icons, and metascore when an API key is set.

**Use cases:** Discover new games, find specific titles, browse a genre.

**Troubleshooting:** "query required for search" — you forgot the `query` parameter.

---

## Tutorial 2: Live Player Count (No API Key)

**Goal:** See how many people are playing a game right now.

**Tool:** `steam_stats`

**Arguments:**
```json
{"operation": "players", "app_id": 440}
```

**Expected output:**
```json
{
  "success": true,
  "message": "Concurrent players for app 440: 85,432",
  "data": {"player_count": 85432}
}
```

**Prefab:** `show_player_count_card(app_id=440)`

**Popular app IDs for quick checks:**
- 440 — Team Fortress 2
- 570 — Dota 2
- 730 — Counter-Strike 2
- 1172470 — Apex Legends
- 271590 — GTA V
- 578080 — PUBG
- 1091500 — Cyberpunk 2077
- 252490 — Rust

**How it works:** `ISteamUserStats/GetNumberOfCurrentPlayers` returns the concurrent player count. This is public — no API key needed.

**Troubleshooting:** Returns 0 or very low count for apps that don't report player data (some single-player games, unreleased titles).

---

## Tutorial 3: Game Details & Metadata

**Goal:** Get full store page metadata for a specific game.

**Tool:** `steam_library`

**Arguments:**
```json
{"operation": "details", "app_id": 570, "country": "US"}
```

**Expected output:**
```json
{
  "success": true,
  "message": "App details for 570: Dota 2 — ...",
  "data": {
    "name": "Dota 2",
    "steam_appid": 570,
    "short_description": "Every day, millions of players worldwide...",
    "developers": ["Valve"],
    "publishers": ["Valve"],
    "genres": [{"id": "1", "description": "Action"}, {"id": "2", "description": "Free to Play"}, {"id": "23", "description": "Strategy"}],
    "categories": [{"id": 1, "description": "Multi-player"}, {"id": 9, "description": "Co-op"}, {"id": 29, "description": "Steam Trading Cards"}],
    "price_overview": {"currency": "USD", "initial": 0, "final": 0, "discount_percent": 0},
    "release_date": {"coming_soon": false, "date": "Jul 9, 2013"},
    "required_age": 0,
    "supported_languages": "English, ...  (27 languages)",
    "header_image": "https://cdn.cloudflare.steamstatic.com/...",
    "background_raw": "https://cdn.cloudflare.steamstatic.com/...",
    "recommendations": {"total": 1234567},
    "metacritic": {"score": 90, "url": "..."},
    "platforms": {"windows": true, "mac": true, "linux": true}
  }
}
```

**How it works:** `steam_library(operation="details")` calls the Steam store API for app metadata. The `country` parameter affects regional pricing display.

**Use cases:** Research before buying, compare game features, check platform support, discover genres and tags.

**Troubleshooting:** Without an API key, some fields (price overview, detailed genres) may be less rich.

---

## Tutorial 4: My Owned Games

**Goal:** List all games on your Steam account with playtime.

**Prerequisites:** `STEAM_API_KEY` + `STEAM_ID` set. Profile must be public.

**Tool:** `steam_library`

**Arguments:**
```json
{"operation": "owned"}
```

**With include_free:**
```json
{"operation": "owned", "include_free": true}
```

**Expected output:**
```json
{
  "success": true,
  "message": "Found 142 owned games. Top 5: ...",
  "data": {
    "game_count": 142,
    "games": [
      {"appid": 570, "name": "Dota 2", "playtime_forever": 2345, "playtime_2weeks": 12, "img_icon_url": "...", "img_logo_url": "..."},
      {"appid": 440, "name": "Team Fortress 2", "playtime_forever": 890, "playtime_2weeks": 0, "img_icon_url": "...", "img_logo_url": "..."}
    ]
  }
}
```

**Prefix:** `show_library_card()` for visual display.

**How it works:** `IPlayerService/GetOwnedGames` returns all games with total playtime in minutes. The `include_free` parameter adds free-to-play games (excluded by default).

**Use cases:** Audit your library, find games you haven't played, compare libraries with friends.

**Troubleshooting:** "Empty library" — your profile is likely private. Set it to public in Steam privacy settings. Also verify `STEAM_ID` is correct.

---

## Tutorial 5: Recently Played Games

**Goal:** See what you or a friend has been playing recently.

**Tool:** `steam_library`

**Arguments:**
```json
{"operation": "recent", "count": 10}
```

**For another user:**
```json
{"operation": "recent", "steamid": "76561198000000000", "count": 5}
```

**Expected output:**
```json
{
  "success": true,
  "message": "Recently played (5 games): ...",
  "data": {
    "total_count": 5,
    "games": [
      {"appid": 730, "name": "Counter-Strike 2", "playtime_2weeks": 340, "playtime_forever": 1500, "img_icon_url": "...", "img_logo_url": "..."}
    ]
  }
}
```

**How it works:** `IPlayerService/GetRecentlyPlayedGames` returns the last 2 weeks of play activity.

---

## Tutorial 6: Achievement Progress

**Goal:** Check your achievement completion for a game.

**Prerequisites:** `STEAM_API_KEY` + `STEAM_ID`. Profile must be public.

**Tool:** `steam_stats`

**Arguments:**
```json
{"operation": "achievements", "steamid": "", "app_id": 440}
```

(Leave `steamid` empty to use default `STEAM_ID`)

**Expected output:**
```json
{
  "success": true,
  "message": "Achievements for app 440: 120/520 unlocked",
  "data": {
    "playerstats": {
      "achievements": [
        {"apiname": "ACH_WIN_ONE_GAME", "achieved": 1, "unlocktime": 1690000000},
        {"apiname": "ACH_KILL_1000", "achieved": 0, "unlocktime": 0},
        {"apiname": "ACH_MASTER_HEAVY", "achieved": 1, "unlocktime": 1695000000}
      ],
      "gameName": "Team Fortress 2"
    }
  }
}
```

**How it works:** `ISteamUserStats/GetPlayerAchievements` returns per-achievement unlock status and timestamp.

**Use cases:** Track completion progress, find next achievements to hunt, compare with friends.

**Troubleshooting:** "steamid and app_id required" — ensure your `STEAM_ID` is set in env and the profile is public.

---

## Tutorial 7: Global Achievement Rarity (No API Key)

**Goal:** Find the rarest achievements in a game.

**Tool:** `steam_stats`

**Arguments:**
```json
{"operation": "global_percentages", "app_id": 440}
```

**Expected output:**
```json
{
  "success": true,
  "message": "Global achievement percentages for app 440",
  "data": {
    "achievementpercentages": {
      "achievements": [
        {"name": "ACH_WIN_ONE_GAME", "percent": 72.5},
        {"name": "ACH_RARE_FIND", "percent": 2.3},
        {"name": "ACH_LEGENDARY", "percent": 0.1}
      ]
    }
  }
}
```

**How it works:** `ISteamUserStats/GetGlobalAchievementPercentagesForApp` is public — no API key needed.

**Use cases:** Find rare achievements to hunt, gauge game difficulty, see how many players completed the game.

---

## Tutorial 8: Player Profile Lookup

**Goal:** Look up a player's profile information.

**Tool:** `steam_profile`

**Your own profile:**
```json
{"operation": "own"}
```

**Look up by vanity URL (no API key):**
```json
{"operation": "resolve_vanity", "vanity_url": "gaben"}
```
Returns `{"success": true, "data": {"steamid": "76561197960287930", "message": "Resolved successfully"}}`

**Batch player summaries:**
```json
{"operation": "summaries", "steamids": "76561197960287930,76561198000000001"}
```

**Expected output (summaries):**
```json
{
  "success": true,
  "message": "Player summaries for 2 players",
  "data": {
    "players": [
      {"steamid": "76561197960287930", "personaname": "Gaben", "profileurl": "https://steamcommunity.com/id/gaben/", "avatar": "https://...", "personastate": 1, "lastlogoff": 1699999999, "realname": "Gabe Newell", "loccountrycode": "US", "timecreated": 1063407589}
    ]
  }
}
```

**How it works:** `resolve_vanity_url` converts custom URLs to 64-bit Steam IDs. `GetPlayerSummaries` fetches profile data for up to 100 IDs at once.

**Use cases:** Look up friends, verify Steam IDs, check online status, find account age.

---

## Tutorial 9: Friend List

**Goal:** See who's on a Steam user's friend list.

**Prerequisites:** `STEAM_API_KEY`. The target profile must have a public friend list.

**Tool:** `steam_profile`

**Arguments:**
```json
{"operation": "friends", "steamid": "76561198000000000", "relationship": "all"}
```

**Filter to mutual friends only:**
```json
{"operation": "friends", "steamid": "76561198000000000", "relationship": "friend"}
```

**Expected output:**
```json
{
  "success": true,
  "message": "Friends for 76561198000000000: 42 friends",
  "data": {
    "friends": [
      {"steamid": "76561198000000001", "relationship": "friend", "friend_since": 1500000000}
    ]
  }
}
```

**How it works:** `ISteamUser/GetFriendList` returns the friend list with relationship type and friend_since timestamp.

---

## Tutorial 10: Game News & Updates

**Goal:** Check recent news and patch notes for a game.

**Tool:** `steam_store`

**Arguments:**
```json
{"operation": "news", "app_id": 730, "count": 5}
```

**Expected output:**
```json
{
  "success": true,
  "message": "Found 5 news items for app 730",
  "data": {
    "appnews": {
      "appid": 730,
      "newsitems": [
        {"title": "Release Notes for 6/20/2026", "url": "https://steamcommunity.com/...", "contents": " [ PATCH NOTES ] ...", "date": 1720000000, "feed_type": 1}
      ]
    }
  }
}
```

**How it works:** `ISteamNews/GetNewsForApp` returns the most recent news posts. Content is provided as BBCode or plain text.

**Use cases:** Track game updates, read patch notes, follow developer announcements.

---

## Tutorial 11: User Reviews

**Goal:** Read community reviews for a game.

**Tool:** `steam_store`

**Arguments:**
```json
{"operation": "reviews", "app_id": 1091500, "count": 5}
```

**Expected output:** Array of reviews with author Steam ID, recommendation (positive/negative), playtime at review, review text, vote counts.

**How it works:** `ISteamUser/GetAppReviews` (with API key) or the store review API. Reviews include the author's playtime and whether they recommend the game.

---

## Tutorial 12: Workshop Mods Discovery

**Goal:** Browse mods for a game on the Steam Workshop.

**Prerequisites:** `STEAM_API_KEY`

**Tool:** `steam_workshop`

**Arguments:**
```json
{"operation": "query", "app_id": 440, "query": "training", "count": 10, "sort_by": "mostsubscribed"}
```

**Expected output:**
```json
{
  "success": true,
  "message": "Found 10 Workshop items for app 440 (query: 'training')",
  "data": {
    "items": [
      {"publishedfileid": "12345", "title": "tr_walkway_rc2", "file_url": "https://steamcommunity.com/...", "preview_url": "https://steamcommunity.com/...", "subscriptions": 50000, "favorited": 12000, "creator": "76561198000000000", "time_created": 1300000000, "time_updated": 1600000000}
    ]
  }
}
```

**Sort options:** `mostrecent`, `score`, `trend`, `mostsubscribed`, `mostfavorited`.

**Prefab:** `show_workshop_card(app_id=440, query="map")`

---

## Tutorial 13: Workshop Item Details

**Goal:** Get full details for specific Workshop items.

**Tool:** `steam_workshop`

**Arguments:**
```json
{"operation": "item_details", "published_file_ids": "12345,67890"}
```

**Expected output:** Array of items with title, description, file_url, preview_url, creator, file_size, subscriptions, favorited count, time_created, time_updated, tags.

**How it works:** `ISteamRemoteStorage/GetPublishedFileDetails` returns complete metadata for up to 100 published files.

---

## Tutorial 14: Leaderboards

**Goal:** Discover competitive leaderboards for a game.

**Tool:** `steam_stats`

**Arguments:**
```json
{"operation": "leaderboards", "app_id": 440}
```

**Expected output:** Array of leaderboard entries with ID, name, display name, entry count, sort method, display type.

**How it works:** Returns leaderboard metadata. For actual leaderboard entries, the API requires additional calls per-leaderboard.

---

## Tutorial 15: Server Health Check

**Goal:** Verify steam-mcp connectivity and auth status.

**Tool:** `steam_system`

**Arguments:**
```json
{"operation": "status"}
```

**Expected output:**
```json
{
  "success": true,
  "message": "Steam-MCP status: API key OK, Steam ID OK",
  "data": {"has_api_key": true, "has_steam_id": true, "tool_count": 13, "version": "0.2.0"}
}
```

**Prefab:** `show_steam_status_card()`

**SteamCMD detection:**
```json
{"operation": "steamcmd_status"}
```

---

## Tutorial 16: Agentic Multi-Step Workflow

**Goal:** Let the LLM autonomously execute a multi-step Steam query.

**Prerequisites:** Host must support MCP sampling.

**Tool:** `agentic_steam_workflow`

**Arguments:**
```json
{"goal": "Find the top 3 most played free games, then get their player counts and recent reviews"}
```

**Expected output:**
```json
{
  "success": true,
  "message": "Based on Steam data, the top 3 most played free games are...",
  "data": {"goal": "Find the top 3 most played free games..."}
}
```

**How it works:** The host LLM plans a sequence of `steam_store` + `steam_stats` + `steam_store` calls, the server executes them, and results are fed back for summarization.

**Without sampling:** Chain portmanteau tools manually and summarize yourself.

**Example goals for agentic workflows:**
- "Compare my owned games to my wishlist and recommend which ones to buy next based on reviews"
- "Find all Workshop mods for TF2 with over 10000 subscribers and summarize them"
- "Search for space games releasing next month and check their pre-release player counts"
- "Analyze my library: which games have I played most vs least? Any hidden gems with high playtime?"

---

## Tutorial 17: Help & Discovery

**Goal:** Learn about available tools and operations.

**Tool:** `steam_help`

**Brief overview:**
```json
{"level": "brief"}
```

**Full details:**
```json
{"level": "full"}
```

**Operations matrix:**
```json
{"level": "operations"}
```

**MCP Resources:** `resource://steam/capabilities` and `resource://steam/quickstart` provide machine-readable reference.

**MCP Prompts:**
- `steam_library_review(app_id=440)` — Review a game using library + stats tools
- `steam_store_search(default_query="indie")` — Search store + get player counts
- `steam_workshop_browse(app_id=440)` — Browse Workshop with popularity sorting

---

## Tutorial 18: Steamworks Publishing Workflow

**Goal:** Publish a game build to Steam via SteamPipe.

**Prerequisites:** `STEAM_APP_ID`, `STEAM_DEPOT_ID`, `STEAM_USERNAME`, `STEAMCMD_PATH` set. Optional: `STEAMCMD_PASSWORD`, `STEAM_CONTENT_ROOT`.

**Step 1 — Check readiness:**
```json
{"operation": "status"}
```

**Step 2 — Review release checklist:**
```json
{"operation": "checklist"}
```

**Step 3 — Pricing guidance:**
```json
{"operation": "monetization"}
```

**Step 4 — Validate build folder:**
```json
{"operation": "validate_build", "content_root": "C:/builds/my-game/win"}
```

**Step 5 — Generate VDF files:**
```json
{"operation": "generate_vdf", "content_root": "C:/builds/my-game/win", "branch": "beta", "desc": "Beta build v0.3.1"}
```

**Step 6 — Upload (dry run first!):**
```json
{"operation": "upload_prerelease", "content_root": "C:/builds/my-game/win", "dry_run": true}
```

**Step 7 — Upload for real:**
```json
{"operation": "upload_prerelease", "content_root": "C:/builds/my-game/win", "dry_run": false}
```

**Step 8 — Upload to live (default branch):**
```json
{"operation": "upload_release", "content_root": "C:/builds/my-game/win", "dry_run": false}
```

**How it works:** `steam_publish` wraps the SteamPipe workflow: validate content → generate depot/app build VDFs → invoke `steamcmd` for upload. All upload operations default to `dry_run=true` for safety.

**Cross-repo integration:** godot-mcp can call `steam_publish` directly to ship Godot games to Steam. Builds are staged in `FLEET_EXCHANGE_ROOT` for cross-repo handoff.

**Troubleshooting:**
- "STEAMCMD_PATH not set" — steamcmd.exe not found. Install from https://developer.valvesoftware.com/wiki/SteamCMD
- "STEAM_APP_ID not configured" — set your game's App ID from Steamworks partner dashboard
- Upload fails — check `STEAM_USERNAME` and `STEAMCMD_PASSWORD`; you may need an SSFN guard code

---

## Tutorial 19: Reading MCP Resources

**Resource URIs** provide static reference data without making API calls:

- **`resource://steam/capabilities`** — Full tool list, transport modes, auth requirements
- **`resource://steam/quickstart`** — Step-by-step getting started guide

Use `resources/list` and `resources/read` MCP protocol methods to access these. The web dashboard also serves them via the REST API.

---

## Tutorial 20: Web Dashboard

**Starting the full stack:**
```powershell
just serve
.\webapp\start.ps1
```

Open `http://localhost:11021`

**Dashboard features:**
- **Chat:** Hybrid LLM (Ollama) + rule-based fallback. Ask natural language questions about Steam.
- **Tool Console:** Call any portmanteau tool directly with a form UI.
- **Settings:** Configure `STEAM_API_KEY`, `STEAM_ID`, chat mode (`hybrid`/`llm`/`rules`), AI endpoint/model.
- **Status:** Real-time connectivity test and health indicators.

### Ollama Setup for Web Chat

1. Install Ollama and pull a model: `ollama pull llama3.1:8b`
2. Set `STEAM_CHAT_MODE=hybrid` (default)
3. Optional: Configure `AI_MODEL=llama3.1:8b`, `AI_ENDPOINT=http://localhost:11434/v1`

The chat mode `rules` disables LLM and uses keyword-based intent routing only (no GPU needed).

---

## Tauri Native App

Steam-MCP ships a Windows desktop app via Tauri 2:

```powershell
.\native\build.ps1
```

Produces a single NSIS installer with embedded backend on port 11020. The native app includes the React dashboard, MCP server, and SteamCMD integration for publishing.

Dev mode:
```powershell
just serve
just native-dev
```

---

## Getting a Steam Web API Key

1. Visit https://steamcommunity.com/dev/apikey
2. Sign in with your Steam account
3. Enter a domain name (localhost is fine for dev)
4. Accept the terms
5. Copy the generated key into `STEAM_API_KEY`

**Profile visibility:** For library and achievement queries to work, the target Steam profile must be public. Set this in Steam → Profile → Edit Profile → Privacy Settings → "Public."

**Finding your Steam ID:**
- Open Steam client → click your profile name → the URL shows a number (e.g., `7656119xxxxxxxxxx`)
- Or use `steam_profile(operation="resolve_vanity", vanity_url="your-custom-url")`

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| "API key missing" | STEAM_API_KEY not set | Set env var; profile/library/wishlist require it |
| Empty library | Profile is private or wrong STEAM_ID | Make profile public; verify Steam ID |
| Empty wishlist | Profile is private | Make profile public in Steam privacy settings |
| Store search returns no results | Query too specific or misspelled | Try broader terms |
| Player count is 0 | App doesn't report player counts | Some single-player games don't report |
| "steamid required" | Missing Steam ID for operation | Pass `steamid` parameter or set `STEAM_ID` env |
| "app_id required" | Missing app ID for operation | Pass `app_id=440` (or appropriate game ID) |
| Publishing upload hangs | steamcmd needs credentials | Set `STEAMCMD_PASSWORD` or use SSFN guard code |
| LLM chat falls back to rules | Ollama not running | Start Ollama or set `STEAM_CHAT_MODE=rules` |
| MCP HTTP 404 | Wrong endpoint | Use `/mcp` not `/sse`; run `just serve` |
| Prefab shows dict not card | prefab-ui not installed | Run `uv add prefab-ui`; check `STEAM_PREFAB_APPS` |
| Rate limited | Too many API calls | Space out calls; batch where possible |

### Extended Diagnostics

For deeper troubleshooting, use:

```json
{"operation": "status"}
```
via `steam_system`. The status response confirms which environment variables are set. If `has_api_key` is false, `STEAM_API_KEY` is missing. If `has_steam_id` is false, `STEAM_ID` is unset.

---

## Cross-Repo Integration Patterns

### godot-mcp → steam-mcp

Godot game builder calls `steam_publish` to ship games to Steam:
```python
# In godot-mcp context, after building the game:
steam_publish(operation="upload_prerelease", content_root="C:/exchange/godot-mcp/my-game/win", dry_run=False)
```

### Fleet Exchange

Build files flow through `FLEET_EXCHANGE_ROOT`:
```
C:/exchange/
  ├── godot-mcp/          # Godot builds
  │   └── my-game/
  │       └── win/        # Windows export
  └── steam-mcp/          # Steam depot staging
      └── uploads/
```

Set `FLEET_EXCHANGE_ROOT=C:/exchange` to enable cross-repo build sharing.

---

## Advanced Query Patterns

### Pattern 1: Game Discovery Pipeline

Discover new games systematically:

```python
# Step 1: Search for a genre
store_results = steam_store(operation="search", query="RPG open world", count=5)

# Step 2: For each result, get details
for result in store_results.data.results:
    details = steam_library(operation="details", app_id=result.appid)

# Step 3: Get player counts
for result in store_results.data.results:
    players = steam_stats(operation="players", app_id=result.appid)

# Step 4: Get reviews
for result in store_results.data.results:
    reviews = steam_store(operation="reviews", app_id=result.appid, count=5)
```

### Pattern 2: Friend Comparison

Compare your library with a friend's:

```python
# Step 1: Get your library
my_library = steam_library(operation="owned")
my_games = set(g.appid for g in my_library.data.games)

# Step 2: Get friend's library
friend_library = steam_library(operation="owned", steamid="<friend_id>")
friend_games = set(g.appid for g in friend_library.data.games)

# Step 3: Compute differences
only_mine = my_games - friend_games
only_theirs = friend_games - my_games
shared = my_games & friend_games
```

### Pattern 3: Achievement Hunting

Find rare achievements you haven't unlocked:

```python
# Step 1: Get your achievements for a game
my_achievements = steam_stats(operation="achievements", steamid="", app_id=440)

# Step 2: Get global percentages
global_stats = steam_stats(operation="global_percentages", app_id=440)

# Step 3: Cross-reference: find locked achievements with <5% global rate
rare_locked = []
for ach in my_achievements.data.playerstats.achievements:
    if not ach.achieved:
        global_pct = next((g.percent for g in global_stats.data.achievements if g.name == ach.apiname), 100)
        if global_pct < 5:
            rare_locked.append({"name": ach.apiname, "global_rate": global_pct})
```

### Pattern 4: Store Research Before Purchase

Make informed buying decisions:

```python
# Step 1: Get full details
details = steam_library(operation="details", app_id=1091500)

# Step 2: Check reviews
reviews = steam_store(operation="reviews", app_id=1091500, count=20)

# Step 3: Check player activity
players = steam_stats(operation="players", app_id=1091500)

# Step 4: Check achievement support
global_achs = steam_stats(operation="global_percentages", app_id=1091500)

# Step 5: Check Workshop community
workshop = steam_workshop(operation="query", app_id=1091500, query="", count=5)

# Decision factors:
# - Price within budget?
# - Review sentiment positive?
# - Active player base?
# - Achievement variety?
# - Workshop community active?
```

### Pattern 5: Steamworks Publishing Pipeline

Full game publishing workflow:

```python
# 1. Pre-flight checks
status = steam_publish(operation="status")
checklist = steam_publish(operation="checklist")
monetization = steam_publish(operation="monetization")

# 2. Build validation
validation = steam_publish(operation="validate_build", content_root="C:/builds/my-game")

# 3. Dry-run VDF generation
vdf_dry = steam_publish(operation="generate_vdf", content_root="C:/builds/my-game", branch="beta", desc="Test build")

# 4. Dry-run upload
upload_dry = steam_publish(operation="upload_prerelease", content_root="C:/builds/my-game", dry_run=true)

# 5. If all passes, do the real upload
upload_real = steam_publish(operation="upload_prerelease", content_root="C:/builds/my-game", dry_run=false)

# 6. For release:
release_dry = steam_publish(operation="upload_release", content_root="C:/builds/my-game", dry_run=true)
# ... review, then:
release_real = steam_publish(operation="upload_release", content_root="C:/builds/my-game", dry_run=false)
```

## Understanding Steam Data Types

### Steam ID Formats

Steam uses 64-bit numeric IDs internally. You'll encounter three formats:

| Format | Example | How to get |
|--------|---------|------------|
| SteamID64 | 76561197960287930 | `resolve_vanity` returns this |
| SteamID3 | [U:1:12345678] | Used in community URLs |
| Custom URL | gaben | `resolve_vanity` input |

Always use SteamID64 when calling `steam_profile`, `steam_library`, or `steam_stats`.

### Playtime Fields

- **`playtime_forever`** — Total minutes played since the game was added to the library
- **`playtime_2weeks`** — Minutes played in the last 2 weeks (only on `recent` operation)
- **Conversion**: Divide by 60 for hours. A value of 0 for `playtime_forever` means the game was added but never launched.

### Achievement Status

- `achieved: 1` — Unlocked
- `achieved: 0` — Locked
- `unlocktime: 0` — Never unlocked (if achieved=0) or unlock time unknown (rare)
- `unlocktime: <timestamp>` — Unix timestamp of when the achievement was earned

### Store Price Fields

- `price_overview.initial` — Original price (before discount)
- `price_overview.final` — Current price (after discount)
- `price_overview.discount_percent` — Discount percentage (0 = no discount)
- `price_overview.currency` — ISO currency code (USD, EUR, GBP, etc.)
- Prices are in the smallest currency unit (cents for USD/EUR)

### Player Count Accuracy

The `players` operation returns the current concurrent player count as reported by Steam. This number:
- Updates approximately every 5 minutes
- May not include players in offline mode
- Is approximate — Valve doesn't guarantee accuracy
- Returns 0 for apps that don't support the stat (some single-player games)

## MCP Protocol Usage

### Calling Tools via REST

The `/api/tools/{name}/call` endpoint allows direct tool invocation without an MCP client:

```bash
curl -X POST http://localhost:11020/api/tools/steam_store/call \
  -H "Content-Type: application/json" \
  -d '{"operation": "search", "query": "Godot", "count": 5}'
```

### Resources via REST

```bash
curl http://localhost:11020/api/resources/steam/capabilities
curl http://localhost:11020/api/resources/steam/quickstart
```

### Discovery Manifest

The manifest at `/.well-known/mcp/manifest.json` enables automatic server discovery by MCP clients:

```bash
curl http://localhost:11020/.well-known/mcp/manifest.json
```

Returns JSON with server name, version, transport types, tool listing, and auth requirements.

## Steam API Limitations & Best Practices

### Rate Limits

Steam does not publish official rate limits, but community experience suggests:

- **Store API:** ~200 requests per 5 minutes per IP
- **Player Service:** More restrictive — batch queries with `summaries`
- **ISteamUserStats:** Generally generous for public endpoints
- **Workshop:** Similar to store API limits

**Mitigation strategies:**
- Batch player lookups with comma-separated IDs (up to 100)
- Cache app details (they change rarely)
- Space out bulk operations with small delays
- Use agentic workflows for complex multi-step queries (the LLM naturally spaces calls)

### Profile Privacy

Steam profiles have three privacy levels:
- **Public:** All data accessible via API
- **Friends Only:** Only friends can see game library and achievements
- **Private:** Only basic profile info (name, avatar) is visible

If `steam_library` or `steam_stats(operation="achievements")` returns empty for a known valid Steam ID, the profile is likely private. Guide the user to adjust their Steam privacy settings.

### Game Visibility

Even with a public profile:
- Free-to-play games may not appear in `owned` unless `include_free=true`
- Games marked as "private" in Steam library settings are hidden from the API
- Recently refunded games may still appear temporarily

### Store vs Library Data

There are two distinct app data sources:
- **Store API** (`steam_library(operation="details")`): Commercial metadata — price, description, genres, platforms, age ratings
- **Player Service** (`steam_library(operation="owned")`): Personal data — playtime, achievement count, last played

They serve different purposes and return different fields. Use `details` for research, `owned` for personal library queries.

## SteamCMD & Publishing Details

### SteamCMD Setup

1. Download steamcmd from https://developer.valvesoftware.com/wiki/SteamCMD
2. Extract to a folder (e.g., `C:\steamcmd\`)
3. Set `STEAMCMD_PATH=C:\steamcmd\steamcmd.exe`
4. First run: `steamcmd.exe` — it will self-update

### SSFN Authentication

If you have Steam Guard enabled (recommended), you'll need an SSFN file:
1. Log into Steam on your development machine
2. Copy the `.ssfn` file from your Steam folder
3. Place it next to `steamcmd.exe`

This avoids the need to store your password in `STEAMCMD_PASSWORD`.

### Depot vs App Build VDFs

- **`app_build.vdf`** — Defines which depots are included in the build, build description, and target branch
- **`depot_build.vdf`** — Defines the file mapping for a specific depot (ContentRoot, FileMapping, FileExclusion)

The `generate_vdf` operation creates both files. You can manually edit them before upload for custom file mappings.

### Build Branches

- **`default`** — The live/public branch that all users see
- **`beta`** — An opt-in beta branch (password-protected or open)
- Custom branch names can be created in the Steamworks partner dashboard

Always upload to `beta` first, test, then promote to `default` for release.

## Regional Pricing & Store Differences

Steam store data varies by region. The `country` parameter on `steam_library(operation="details")` affects:
- Displayed price and currency
- Age rating requirements
- Content availability (some games are region-locked)
- Language support listings

Common country codes: `US`, `DE`, `GB`, `JP`, `BR`, `RU`, `CN`, `KR`, `AU`, `CA`.

Without a key, prices default to US region. With a key, the region may auto-detect from your account.

## Web Dashboard Features

The React dashboard at `http://localhost:11021` includes:

### Chat Interface
- Text input with enter-to-send
- Markdown rendering of tool responses
- Hybrid LLM fallback indicator
- Suggestion chips for common queries

### Tool Console
- Dropdown to select any portmanteau tool
- Dynamic form based on operation selection
- JSON response viewer with syntax highlighting
- Copy-to-clipboard for tool calls

### Settings Panel
- API key input (masked, stored in-memory only)
- Steam ID input
- Chat mode selector (hybrid/llm/rules)
- AI endpoint and model configuration
- Connectivity test button

### Status Bar
- Backend connectivity indicator (green/red dot)
- Tool count display
- Version number
- GitHub link

## Performance Optimization

### Reducing API Calls

- **Cache app details locally:** Game metadata changes infrequently. Cache results from `steam_library(operation="details")` for 1+ hour.
- **Batch player summaries:** Instead of calling `steam_profile(operation="summaries")` once per Steam ID, pass up to 100 comma-separated IDs in a single call.
- **Pre-filter on server side:** Use `count` and `sort_by` parameters to limit result size rather than fetching everything and filtering client-side.

### Common Query Optimizations

| Inefficient | Efficient | Why |
|-------------|-----------|-----|
| 10 individual player lookups | 1 batch `summaries` call | 10x fewer API calls |
| Full library + client-side filter | Use `steam_store(operation="search")` | Store search is faster |
| Repeated `details` calls | Cache results for 1 hour | Game metadata is stable |
| Workshop query without sort | Always specify `sort_by` | Reduces pagination |

## Fleet Integration Details

### Cross-Repo Handoff Protocol

When godot-mcp ships a game to Steam:

1. godot-mcp exports the game build to `FLEET_EXCHANGE_ROOT/godot-mcp/<game>/win/`
2. godot-mcp calls `steam_publish(operation="upload_prerelease", content_root="<exchange_path>")`
3. steam-mcp validates the build, generates VDFs, and invokes steamcmd
4. Results are returned to godot-mcp for display

### Port Conventions

- Backend: **11020** (FastAPI + MCP HTTP)
- Frontend: **11021** (Vite dev)
- Tauri native app uses port 11020 internally
- No port conflicts with other fleet servers

### Health Integration

The `/api/status` endpoint is designed for fleet health monitoring. Use `meta-mcp` or `monitoring-mcp` to periodically probe steam-mcp's status and alert on API key expiration, connectivity loss, or SteamCMD misconfiguration.

## Glossary

| Term | Definition |
|------|------------|
| **SteamID64** | 64-bit numeric Steam user identifier (e.g., 76561197960287930) |
| **App ID** | Numeric identifier for a Steam application (game, DLC, software) |
| **Vanity URL** | Custom Steam community URL (e.g., steamcommunity.com/id/gaben) |
| **Depot** | A logical grouping of game files within a Steam app |
| **SteamPipe** | Valve's content delivery system for game builds |
| **VDF** | Valve Data Format — key-value config files for SteamPipe |
| **SteamCMD** | Command-line Steam client for dedicated servers and publishing |
| **SSFN** | Steam Guard sentry file for passwordless authentication |
| **ISteamUser** | Steam Web API interface for user/profile data |
| **ISteamUserStats** | Steam Web API interface for achievements and player counts |
| **ISteamRemoteStorage** | Steam Web API interface for Workshop (UGC) |
| **Published File ID** | Unique identifier for a Workshop item |
| **Concurrent Players** | Number of users currently in-game (approximate) |

