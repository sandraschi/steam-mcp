export default function Help() {
  const portmanteau = [
    ["steam_profile", "own, summaries, friends, resolve_vanity", "Key for most"],
    ["steam_library", "owned, recent, details, wishlist", "Key for owned/wishlist"],
    ["steam_stats", "achievements, global_percentages, players, leaderboards", "Mixed"],
    ["steam_store", "news, search, reviews", "No key for news/search"],
    ["steam_workshop", "query, item_details", "Key required"],
    ["steam_system", "status, steamcmd_status", "No key"],
    ["steam_help", "brief, full, operations", "No key"],
    ["agentic_steam_workflow", "goal", "Sampling host"],
  ];

  return (
    <div className="max-w-3xl">
      <h1 className="text-2xl font-bold mb-4">Help</h1>

      <div className="space-y-6 text-sm text-zinc-300">
        <section className="rounded-lg border border-zinc-800 bg-zinc-900 p-4">
          <h2 className="text-lg font-semibold mb-2">Getting Started</h2>
          <ol className="list-decimal list-inside space-y-1 text-zinc-400">
            <li>Get a Steam Web API key at <a href="https://steamcommunity.com/dev/apikey" className="text-blue-400 underline">steamcommunity.com/dev/apikey</a></li>
            <li>Set <code className="text-blue-400">STEAM_API_KEY</code> and <code className="text-blue-400">STEAM_ID</code></li>
            <li>Run <code className="text-blue-400">just serve</code> or <code className="text-blue-400">start.ps1</code></li>
            <li>MCP endpoint: <code className="text-blue-400">http://localhost:11020/mcp</code></li>
            <li>Use the <strong>Chat</strong> page to run tools from the dashboard</li>
          </ol>
        </section>

        <section className="rounded-lg border border-zinc-800 bg-zinc-900 p-4">
          <h2 className="text-lg font-semibold mb-2">Portmanteau tools (v0.2.0)</h2>
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="text-zinc-500 border-b border-zinc-800">
                <th className="py-1">Tool</th><th className="py-1">Operations</th><th className="py-1">Auth</th>
              </tr>
            </thead>
            <tbody className="text-zinc-400">
              {portmanteau.map(([tool, ops, auth]) => (
                <tr key={tool} className="border-b border-zinc-800/50">
                  <td className="py-1"><code className="text-blue-400">{tool}</code></td>
                  <td className="py-1">{ops}</td>
                  <td className="py-1">{auth}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>

        <section className="rounded-lg border border-zinc-800 bg-zinc-900 p-4">
          <h2 className="text-lg font-semibold mb-2">Publishing on Steam</h2>
          <p className="text-zinc-400">
            See <a href="https://github.com/sandraschi/mcp-central-docs/blob/main/docs/gamedev/STEAM_PUBLISHING.md" className="text-blue-400 underline">STEAM_PUBLISHING.md</a> in mcp-central-docs.
            Set <code className="text-blue-400">STEAMCMD_PATH</code> and run <code className="text-blue-400">steam_system(operation=&apos;steamcmd_status&apos;)</code>.
          </p>
        </section>
      </div>
    </div>
  );
}
