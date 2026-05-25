import { useQuery } from "@tanstack/react-query";
import { getStatus, apiGet } from "@/lib/api";

export default function Dashboard() {
  const { data: status } = useQuery({ queryKey: ["status"], queryFn: getStatus });

  return (
    <div className="max-w-3xl">
      <h1 className="text-2xl font-bold mb-4">Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
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
          <p className="text-xs text-zinc-500 uppercase tracking-wide">Version</p>
          <p className="text-lg font-semibold mt-1 text-blue-400">{status?.version ?? "—"}</p>
        </div>
      </div>

      <div className="rounded-lg border border-zinc-800 bg-zinc-900 p-6">
        <h2 className="text-lg font-semibold mb-2">Available Tools</h2>
        <p className="text-sm text-zinc-400 mb-4">
          Steam-MCP exposes 16 tools across 5 categories. Connect via MCP client or use the REST API.
        </p>
        <div className="grid grid-cols-2 gap-3 text-sm">
          {[
            { cat: "Profile", tools: "get_own_profile, get_player_summaries, get_friend_list, resolve_vanity_url" },
            { cat: "Library", tools: "get_owned_games, get_recently_played_games, get_app_details" },
            { cat: "Stats", tools: "get_player_achievements, get_global_achievement_percentages, get_number_of_current_players, get_game_leaderboards" },
            { cat: "Store", tools: "get_news_for_app, search_store" },
            { cat: "Workshop", tools: "query_workshop_items" },
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
