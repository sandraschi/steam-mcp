import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { apiGet } from "@/lib/api";

export default function Games() {
  const [steamId, setSteamId] = useState("");
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ["owned-games", steamId],
    queryFn: () => apiGet<{ success: boolean; data: { games: unknown[] } }>(`/tools/owned_games/call`),
    enabled: false,
  });

  return (
    <div className="max-w-4xl">
      <h1 className="text-2xl font-bold mb-4">Game Library</h1>
      <div className="flex gap-2 mb-6">
        <input
          className="flex-1 rounded border border-zinc-700 bg-zinc-900 px-3 py-2 text-sm"
          placeholder="Enter Steam ID (or set STEAM_ID env)"
          value={steamId}
          onChange={(e) => setSteamId(e.target.value)}
        />
        <button
          className="rounded bg-blue-600 px-4 py-2 text-sm font-medium hover:bg-blue-500 transition-colors"
          onClick={() => refetch()}
        >
          Load Games
        </button>
      </div>

      <div className="text-sm text-zinc-500 mb-4">
        Use the MCP tool <code className="text-blue-400">get_owned_games</code> from your AI client to browse
        your full library. This page shows a placeholder — full integration via the REST bridge is WIP.
      </div>

      <div className="rounded-lg border border-zinc-800 bg-zinc-900 p-8 text-center text-zinc-500">
        {isLoading ? "Loading..." : "Enter a Steam ID and click Load Games to fetch your library via the MCP API."}
      </div>
    </div>
  );
}
