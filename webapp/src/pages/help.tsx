export default function Help() {
  return (
    <div className="max-w-3xl">
      <h1 className="text-2xl font-bold mb-4">Help</h1>

      <div className="space-y-6 text-sm text-zinc-300">
        <section className="rounded-lg border border-zinc-800 bg-zinc-900 p-4">
          <h2 className="text-lg font-semibold mb-2">Getting Started</h2>
          <ol className="list-decimal list-inside space-y-1 text-zinc-400">
            <li>Get a Steam Web API key at <a href="https://steamcommunity.com/dev/apikey" className="text-blue-400 underline">steamcommunity.com/dev/apikey</a></li>
            <li>Set <code className="text-blue-400">STEAM_API_KEY</code> environment variable</li>
            <li>Set <code className="text-blue-400">STEAM_ID</code> with your 64-bit Steam ID</li>
            <li>Start the server with <code className="text-blue-400">uv run python -m steam_mcp.server --http --port 11020</code></li>
            <li>Connect your MCP client to <code className="text-blue-400">http://localhost:11020/mcp</code></li>
          </ol>
        </section>

        <section className="rounded-lg border border-zinc-800 bg-zinc-900 p-4">
          <h2 className="text-lg font-semibold mb-2">Tools Overview</h2>
          <p className="text-zinc-400 mb-2">
            16 tools across 5 categories. No auth needed for store/news tools. STEAM_API_KEY required for profile, library, stats, and workshop.
          </p>
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="text-zinc-500 border-b border-zinc-800">
                <th className="py-1">Category</th><th className="py-1">Tool</th><th className="py-1">Key Required</th>
              </tr>
            </thead>
            <tbody className="text-zinc-400">
              {[
                ["Profile", "get_own_profile", "Yes"],
                ["Profile", "get_player_summaries", "Yes"],
                ["Profile", "get_friend_list", "Yes"],
                ["Profile", "resolve_vanity_url", "Yes"],
                ["Library", "get_owned_games", "Yes"],
                ["Library", "get_recently_played_games", "Yes"],
                ["Library", "get_app_details", "No"],
                ["Stats", "get_player_achievements", "Yes"],
                ["Stats", "get_global_achievement_percentages", "No"],
                ["Stats", "get_number_of_current_players", "No"],
                ["Stats", "get_game_leaderboards", "Yes"],
                ["Store", "get_news_for_app", "No"],
                ["Store", "search_store", "No"],
                ["Workshop", "query_workshop_items", "Yes"],
              ].map(([cat, tool, key]) => (
                <tr key={tool} className="border-b border-zinc-800/50">
                  <td className="py-1 text-zinc-500">{cat}</td>
                  <td className="py-1"><code className="text-blue-400">{tool}</code></td>
                  <td className="py-1">{key === "Yes" ? "✓" : "—"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>

        <section className="rounded-lg border border-zinc-800 bg-zinc-900 p-4">
          <h2 className="text-lg font-semibold mb-2">Publishing Godot Games to Steam</h2>
          <p className="text-zinc-400">
            Use <a href="https://godotsteam.com" className="text-blue-400 underline">GodotSteam</a> for Steamworks integration in Godot 4.x.
            Upload builds via SteamPipe (<code className="text-blue-400">steamcmd.exe</code>).
            $100 Steam Direct fee per game. 70/30 revenue split.
          </p>
        </section>
      </div>
    </div>
  );
}
