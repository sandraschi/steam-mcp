import { useQuery } from "@tanstack/react-query";
import { callTool, getStatus } from "@/lib/api";

export default function Profile() {
  const { data: status } = useQuery({ queryKey: ["status"], queryFn: getStatus });
  const { data: profile, refetch, isFetching, error } = useQuery({
    queryKey: ["profile"],
    queryFn: () => callTool("steam_profile", { operation: "own" }),
    enabled: false,
  });

  const player = (profile?.data as { players?: { personaname?: string; steamid?: string; profileurl?: string }[] })?.players?.[0];

  return (
    <div className="max-w-2xl">
      <h1 className="text-2xl font-bold mb-4">Profile</h1>
      <div className="rounded-lg border border-zinc-800 bg-zinc-900 p-6 space-y-4">
        {!status?.has_api_key && (
          <p className="text-sm text-yellow-400">Configure STEAM_API_KEY and STEAM_ID, then reload.</p>
        )}
        <button
          type="button"
          className="rounded bg-blue-600 px-4 py-2 text-sm hover:bg-blue-500 disabled:opacity-50"
          disabled={!status?.has_api_key || isFetching}
          onClick={() => refetch()}
        >
          {isFetching ? "Loading…" : "Load my profile"}
        </button>
        {error && <p className="text-red-400 text-sm">{String(error)}</p>}
        {profile && !profile.success && (
          <p className="text-red-400 text-sm">{profile.message}</p>
        )}
        {player && (
          <div className="text-sm text-zinc-300">
            <p className="text-lg font-semibold text-white">{player.personaname}</p>
            <p className="text-zinc-500">Steam ID: {player.steamid}</p>
            {player.profileurl && (
              <a href={player.profileurl} className="text-blue-400 underline" target="_blank" rel="noreferrer">
                Open Steam profile
              </a>
            )}
          </div>
        )}
        {profile?.message && player && (
          <pre className="text-xs text-zinc-500 whitespace-pre-wrap">{profile.message}</pre>
        )}
      </div>
    </div>
  );
}
