# Steam-MCP — Common Workflows

## Workflow: Indie discovery

1. `steam_store` → `search` with genre keywords
2. For top hits, `steam_library` → `details` for each `app_id`
3. `steam_stats` → `players` for popularity signal
4. Summarize for user with links (app IDs)

## Workflow: Account audit

1. `steam_system` → `status` (verify key + ID)
2. `steam_profile` → `own`
3. `steam_library` → `owned`
4. `steam_library` → `wishlist`
5. Highlight top playtime games

## Workflow: Live service monitoring

1. Pick `app_id` (e.g. 440 TF2, 570 Dota)
2. Poll `steam_stats` → `players` (respect rate limits)
3. Optional: `steam_store` → `news` for context

## Workflow: Workshop mod hunt

1. Confirm API key
2. `steam_workshop` → `query` with `app_id` + search terms
3. `steam_workshop` → `item_details` for selected `publishedfileid`
4. Prefab: `show_workshop_card`

## Workflow: Publishing lane check

1. `steam_system` → `steamcmd_status`
2. Report SteamCMD path detection and version hints

## Workflow: Agentic (sampling hosts)

1. `agentic_steam_workflow(goal="…")` with clear goal string
2. If sampling fails, decompose into manual portmanteau chain
3. Use `steam_help(level="operations")` when stuck
