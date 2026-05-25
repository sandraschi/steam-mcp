import { useQuery } from "@tanstack/react-query";
import { getStatus } from "@/lib/api";

export default function Settings() {
  const { data: status } = useQuery({ queryKey: ["status"], queryFn: getStatus });

  return (
    <div className="max-w-2xl">
      <h1 className="text-2xl font-bold mb-4">Settings</h1>

      <div className="space-y-4">
        <div className="rounded-lg border border-zinc-800 bg-zinc-900 p-4">
          <label className="text-sm font-medium text-zinc-300">STEAM_API_KEY</label>
          <p className="text-xs text-zinc-500 mt-1">
            {status?.has_api_key
              ? "Configured via environment variable."
              : "Not set. Get your key at steamcommunity.com/dev/apikey and set as STEAM_API_KEY env var."}
          </p>
        </div>

        <div className="rounded-lg border border-zinc-800 bg-zinc-900 p-4">
          <label className="text-sm font-medium text-zinc-300">STEAM_ID</label>
          <p className="text-xs text-zinc-500 mt-1">
            {status?.has_steam_id
              ? "Configured."
              : "Optional. Set STEAM_ID env var with your 64-bit Steam ID for profile tools."}
          </p>
        </div>

        <div className="rounded-lg border border-zinc-800 bg-zinc-900 p-4">
          <label className="text-sm font-medium text-zinc-300">Ports</label>
          <p className="text-xs text-zinc-500 mt-1">
            Backend: 11020 | Frontend: 11021 | MCP HTTP: 11020/mcp
          </p>
        </div>
      </div>
    </div>
  );
}
