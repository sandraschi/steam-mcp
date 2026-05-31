import { useQuery, useMutation } from "@tanstack/react-query";
import { callTool, getStatus } from "@/lib/api";

export default function Settings() {
  const { data: status, refetch } = useQuery({ queryKey: ["status"], queryFn: getStatus });

  const testPublic = useMutation({
    mutationFn: () => callTool("steam_store", { operation: "search", query: "Portal", count: 3 }),
  });

  const testSystem = useMutation({
    mutationFn: () => callTool("steam_system", { operation: "status" }),
  });

  return (
    <div className="max-w-2xl">
      <h1 className="text-2xl font-bold mb-4">Settings</h1>

      <div className="space-y-4">
        <div className="rounded-lg border border-zinc-800 bg-zinc-900 p-4">
          <label className="text-sm font-medium text-zinc-300">STEAM_API_KEY</label>
          <p className="text-xs text-zinc-500 mt-1">
            {status?.has_api_key
              ? "Configured via environment variable."
              : "Not set. Get your key at steamcommunity.com/dev/apikey"}
          </p>
        </div>

        <div className="rounded-lg border border-zinc-800 bg-zinc-900 p-4">
          <label className="text-sm font-medium text-zinc-300">STEAM_ID</label>
          <p className="text-xs text-zinc-500 mt-1">
            {status?.has_steam_id ? "Configured." : "Optional — set STEAM_ID for profile/library defaults."}
          </p>
        </div>

        <div className="rounded-lg border border-zinc-800 bg-zinc-900 p-4">
          <label className="text-sm font-medium text-zinc-300">Capabilities</label>
          <ul className="text-xs text-zinc-500 mt-2 space-y-1">
            <li>Prefab: {status?.capabilities?.prefab ? "yes" : "fallback"}</li>
            <li>Agentic: {status?.capabilities?.agentic ? "yes" : "no"}</li>
            <li>Prompts / resources: yes</li>
          </ul>
        </div>

        <div className="rounded-lg border border-zinc-800 bg-zinc-900 p-4 flex flex-wrap gap-2">
          <button
            type="button"
            className="rounded bg-zinc-700 px-3 py-2 text-sm hover:bg-zinc-600"
            onClick={() => refetch()}
          >
            Refresh status
          </button>
          <button
            type="button"
            className="rounded bg-blue-600 px-3 py-2 text-sm hover:bg-blue-500"
            onClick={() => testPublic.mutate()}
            disabled={testPublic.isPending}
          >
            Test store search (no key)
          </button>
          <button
            type="button"
            className="rounded bg-blue-600 px-3 py-2 text-sm hover:bg-blue-500"
            onClick={() => testSystem.mutate()}
            disabled={testSystem.isPending}
          >
            Test system status
          </button>
        </div>

        {(testPublic.data?.message || testSystem.data?.message) && (
          <pre className="text-xs text-zinc-400 whitespace-pre-wrap border border-zinc-800 rounded p-3">
            {testPublic.data?.message || testSystem.data?.message}
          </pre>
        )}
      </div>
    </div>
  );
}
