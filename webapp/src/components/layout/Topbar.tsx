import { useQuery } from "@tanstack/react-query";
import { getStatus } from "@/lib/api";
import { useConnection } from "@/store/connection";

export default function Topbar() {
  const { status: connStatus } = useConnection();
  const { data: status } = useQuery({
    queryKey: ["status"],
    queryFn: getStatus,
    refetchInterval: 15000,
  });

  return (
    <header className="h-12 border-b border-zinc-800 bg-zinc-900/80 backdrop-blur flex items-center justify-between px-4">
      <div className="flex items-center gap-2">
        <span className="text-lg font-bold tracking-tight">Steam-MCP</span>
        {status && <span className="text-xs text-zinc-500">v{status.version}</span>}
      </div>
      <div className="flex items-center gap-4 text-xs">
        <div className="flex items-center gap-1.5">
          <div
            data-testid="connection-status"
            className={`w-2 h-2 rounded-full ${connStatus === "connected" ? "bg-green-500" : connStatus === "connecting" ? "bg-yellow-500 animate-pulse" : "bg-red-500"}`}
          />
          <span data-testid="connection-label" className="capitalize text-zinc-500">
            {connStatus}
          </span>
        </div>
        <span className={status?.has_api_key ? "text-green-400" : "text-yellow-400"}>
          {status?.has_api_key ? "API Key \u2713" : "No Key"}
        </span>
        {status?.has_steam_id && <span className="text-green-400">Steam ID \u2713</span>}
      </div>
    </header>
  );
}
