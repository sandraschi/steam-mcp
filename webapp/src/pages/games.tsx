import { useState } from "react";
import { useQuery, useMutation } from "@tanstack/react-query";
import { callTool, getStatus } from "@/lib/api";

export default function Games() {
  const [steamId, setSteamId] = useState("");
  const [searchQuery, setSearchQuery] = useState("Godot");
  const { data: status } = useQuery({ queryKey: ["status"], queryFn: getStatus });

  const library = useMutation({
    mutationFn: () =>
      callTool("steam_library", {
        operation: "owned",
        steamid: steamId,
      }),
  });

  const search = useMutation({
    mutationFn: () =>
      callTool("steam_store", {
        operation: "search",
        query: searchQuery,
        count: 10,
      }),
  });

  const games = (library.data?.data as { games?: { name?: string; appid?: number; playtime_forever?: number }[] })?.games ?? [];
  const results = (search.data?.data as { results?: { name?: string; appid?: number }[] })?.results ?? [];

  return (
    <div className="max-w-4xl space-y-8">
      <h1 className="text-2xl font-bold">Game Library</h1>

      {!status?.has_api_key && (
        <p className="text-sm text-yellow-400">Set STEAM_API_KEY to load your library.</p>
      )}

      <section className="rounded-lg border border-zinc-800 bg-zinc-900 p-4">
        <h2 className="font-semibold mb-3">Owned games</h2>
        <div className="flex gap-2 mb-4">
          <input
            className="flex-1 rounded border border-zinc-700 bg-zinc-950 px-3 py-2 text-sm"
            placeholder="Steam ID (optional if STEAM_ID set)"
            value={steamId}
            onChange={(e) => setSteamId(e.target.value)}
          />
          <button
            type="button"
            className="rounded bg-blue-600 px-4 py-2 text-sm hover:bg-blue-500"
            onClick={() => library.mutate()}
            disabled={library.isPending}
          >
            Load
          </button>
        </div>
        {library.isError && <p className="text-red-400 text-sm">{String(library.error)}</p>}
        {games.length > 0 && (
          <ul className="text-sm space-y-1 max-h-64 overflow-y-auto">
            {games.slice(0, 50).map((g) => (
              <li key={g.appid} className="text-zinc-300">
                {g.name ?? g.appid} — {Math.floor((g.playtime_forever ?? 0) / 60)}h
              </li>
            ))}
          </ul>
        )}
      </section>

      <section className="rounded-lg border border-zinc-800 bg-zinc-900 p-4">
        <h2 className="font-semibold mb-3">Store search</h2>
        <div className="flex gap-2 mb-4">
          <input
            className="flex-1 rounded border border-zinc-700 bg-zinc-950 px-3 py-2 text-sm"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
          <button
            type="button"
            className="rounded bg-blue-600 px-4 py-2 text-sm hover:bg-blue-500"
            onClick={() => search.mutate()}
            disabled={search.isPending}
          >
            Search
          </button>
        </div>
        {results.length > 0 && (
          <ul className="text-sm space-y-1">
            {results.map((r) => (
              <li key={r.appid} className="text-zinc-300">
                {r.name} <span className="text-zinc-500">({r.appid})</span>
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  );
}
