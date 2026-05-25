import { useQuery } from "@tanstack/react-query";
import { getStatus } from "@/lib/api";

export default function Topbar() {
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
      <div className="flex items-center gap-3 text-xs">
        <span className={status?.has_api_key ? "text-green-400" : "text-yellow-400"}>
          {status?.has_api_key ? "API Key ✓" : "No Key"}
        </span>
        {status?.has_steam_id && <span className="text-green-400">Steam ID ✓</span>}
      </div>
    </header>
  );
}
