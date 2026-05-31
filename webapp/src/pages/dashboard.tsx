import { useQuery } from "@tanstack/react-query";
import { callTool, getStatus } from "@/lib/api";

export default function Dashboard() {
  const { data: status } = useQuery({ queryKey: ["status"], queryFn: getStatus });
  const { data: tf2 } = useQuery({
    queryKey: ["players-440"],
    queryFn: () => callTool("steam_stats", { operation: "players", app_id: 440 }),
    refetchInterval: 60000,
  });

  const playerCount = (tf2?.data as { player_count?: number })?.player_count;

  return (
    <div className="max-w-3xl">
      <h1 className="text-2xl font-bold mb-4">Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div className="rounded-lg border border-zinc-800 bg-zinc-900 p-4">
          <p className="text-xs text-zinc-500 uppercase tracking-wide">API Key</p>
          <p className={`text-lg font-semibold mt-1 ${status?.has_api_key ? "text-green-400" : "text-yellow-400"}`}>
            {status?.has_api_key ? "Configured" : "Missing"}
          </p>
        </div>
        <div className="rounded-lg border border-zinc-800 bg-zinc-900 p-4">
          <p className="text-xs text-zinc-500 uppercase tracking-wide">Steam ID</p>
          <p className={`text-lg font-semibold mt-1 ${status?.has_steam_id ? "text-green-400" : "text-yellow-400"}`}>
            {status?.has_steam_id ? "Set" : "Not Set"}
          </p>
        </div>
        <div className="rounded-lg border border-zinc-800 bg-zinc-900 p-4">
          <p className="text-xs text-zinc-500 uppercase tracking-wide">Tools</p>
          <p className="text-lg font-semibold mt-1 text-blue-400">{status?.tool_count ?? "—"}</p>
        </div>
        <div className="rounded-lg border border-zinc-800 bg-zinc-900 p-4">
          <p className="text-xs text-zinc-500 uppercase tracking-wide">TF2 players</p>
          <p className="text-lg font-semibold mt-1 text-green-400">
            {playerCount != null ? playerCount.toLocaleString() : "—"}
          </p>
        </div>
      </div>

      <div className="rounded-lg border border-zinc-800 bg-zinc-900 p-6">
        <h2 className="text-lg font-semibold mb-2">Portmanteau tools</h2>
        <p className="text-sm text-zinc-400 mb-4">
          v0.2.0 — {status?.tool_count ?? 0} MCP tools. Use the Chat page or connect an MCP client to `/mcp`.
        </p>
        <div className="grid grid-cols-2 gap-3 text-sm">
          {[
            { cat: "Profile", tools: "steam_profile → own, summaries, friends, resolve_vanity" },
            { cat: "Library", tools: "steam_library → owned, recent, details, wishlist" },
            { cat: "Stats", tools: "steam_stats → achievements, global_percentages, players, leaderboards" },
            { cat: "Store", tools: "steam_store → news, search, reviews" },
            { cat: "Workshop", tools: "steam_workshop → query, item_details" },
            { cat: "System", tools: "steam_system, steam_help, agentic_steam_workflow, Prefab cards" },
          ].map((group) => (
            <div key={group.cat} className="rounded border border-zinc-800 p-3">
              <p className="text-blue-400 font-medium mb-1">{group.cat}</p>
              <p className="text-zinc-500 text-xs">{group.tools}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
