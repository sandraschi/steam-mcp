import { useQuery } from "@tanstack/react-query";
import { apiGet, type StatusResponse } from "../lib/api";

export default function Help() {
  const { data: status } = useQuery({
    queryKey: ["status"],
    queryFn: () => apiGet<StatusResponse>("/status"),
  });

  const version = status?.version ?? "0.3.2";

  const portmanteau = [
    ["steam_profile", "own, summaries, friends, resolve_vanity", "API key"],
    ["steam_library", "owned, recent, details, wishlist", "API key"],
    ["steam_stats", "achievements, global_percentages, players, leaderboards", "Mixed"],
    ["steam_store", "news, search, reviews", "No key"],
    ["steam_workshop", "query, item_details", "API key"],
    ["steam_system", "status, steamcmd_status", "No key"],
    ["steam_publish", "status, checklist, monetization, validate, generate_vdf, upload", "No key"],
    ["steam_help", "brief, full, operations", "No key"],
  ];

  const extra = [
    ["agentic_steam_workflow", "Multi-step workflow via LLM sampling", "Sampling host"],
    ["show_steam_status_card", "Prefab: connectivity and auth status", "No key"],
    ["show_library_card", "Prefab: owned games summary", "API key"],
    ["show_store_search_card", "Prefab: store search results", "No key"],
    ["show_workshop_card", "Prefab: Workshop items", "API key"],
    ["show_player_count_card", "Prefab: concurrent player count", "No key"],
  ];

  return (
    <div className="max-w-3xl">
      <h1 className="text-2xl font-bold mb-4">Help</h1>

      <div className="space-y-6 text-sm text-zinc-300">
        <section className="rounded-lg border border-zinc-800 bg-zinc-900 p-4">
          <h2 className="text-lg font-semibold mb-2">Getting Started</h2>
          <ol className="list-decimal list-inside space-y-1 text-zinc-400">
            <li>
              Get a Steam Web API key at{" "}
              <a href="https://steamcommunity.com/dev/apikey" className="text-blue-400 underline">
                steamcommunity.com/dev/apikey
              </a>
            </li>
            <li>
              Set <code className="text-blue-400">STEAM_API_KEY</code> and{" "}
              <code className="text-blue-400">STEAM_ID</code>
            </li>
            <li>
              Run <code className="text-blue-400">just serve</code> or <code className="text-blue-400">start.ps1</code>
            </li>
            <li>
              MCP endpoint: <code className="text-blue-400">http://localhost:11020/mcp</code>
            </li>
            <li>
              Use the <strong>Chat</strong> page to run tools from the dashboard
            </li>
          </ol>
        </section>

        <section className="rounded-lg border border-zinc-800 bg-zinc-900 p-4">
          <h2 className="text-lg font-semibold mb-2">Portmanteau tools (v{version})</h2>
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="text-zinc-500 border-b border-zinc-800">
                <th className="py-1">Tool</th>
                <th className="py-1">Operations</th>
                <th className="py-1">Auth</th>
              </tr>
            </thead>
            <tbody className="text-zinc-400">
              {portmanteau.map(([tool, ops, auth]) => (
                <tr key={tool} className="border-b border-zinc-800/50">
                  <td className="py-1">
                    <code className="text-blue-400">{tool}</code>
                  </td>
                  <td className="py-1">{ops}</td>
                  <td className="py-1">{auth}</td>
                </tr>
              ))}
            </tbody>
          </table>

          <h3 className="text-md font-semibold mt-4 mb-2">Additional Tools</h3>
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="text-zinc-500 border-b border-zinc-800">
                <th className="py-1">Tool</th>
                <th className="py-1">Description</th>
                <th className="py-1">Auth</th>
              </tr>
            </thead>
            <tbody className="text-zinc-400">
              {extra.map(([tool, desc, auth]) => (
                <tr key={tool} className="border-b border-zinc-800/50">
                  <td className="py-1">
                    <code className="text-blue-400">{tool}</code>
                  </td>
                  <td className="py-1">{desc}</td>
                  <td className="py-1">{auth}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>

        <section className="rounded-lg border border-zinc-800 bg-zinc-900 p-4">
          <h2 className="text-lg font-semibold mb-2">Publishing on Steam</h2>
          <p className="text-zinc-400">
            Set <code className="text-blue-400">STEAMCMD_PATH</code> and run{" "}
            <code className="text-blue-400">steam_publish(operation=&apos;checklist&apos;)</code>.
            See{" "}
            <a
              href="https://github.com/sandraschi/mcp-central-docs/blob/main/docs/gamedev/STEAM_PUBLISHING.md"
              className="text-blue-400 underline"
            >
              STEAM_PUBLISHING.md
            </a>{" "}
            in mcp-central-docs for the full guide.
          </p>
          <p className="text-zinc-400 mt-2">
            For Godot game export + Steam upload, use{" "}
            <a
              href="https://github.com/sandraschi/godot-mcp/blob/main/docs/ship-to-steam.md"
              className="text-blue-400 underline"
            >
              godot-mcp Ship to Steam
            </a>
            {" — "}export Windows builds via godot-mcp, then publish via this server.
          </p>
        </section>

        <section className="rounded-lg border border-zinc-800 bg-zinc-900 p-4">
          <h2 className="text-lg font-semibold mb-2">Cross-Fleet Pipeline</h2>
          <p className="text-zinc-400">
            Steam-MCP is the publishing backend for{" "}
            <a href="https://github.com/sandraschi/godot-mcp" className="text-blue-400 underline">godot-mcp</a>.
            Export Windows builds from Godot, stage in the fleet exchange, and upload via SteamPipe:
          </p>
          <pre className="text-xs text-zinc-500 mt-2 font-mono">
godot-mcp (export + stage) → steam-mcp (VDF + steamcmd upload)
          </pre>
        </section>

        <section className="rounded-lg border border-zinc-800 bg-zinc-900 p-4">
          <h2 className="text-lg font-semibold mb-2">Documentation</h2>
          <ul className="list-disc list-inside space-y-1 text-zinc-400">
            <li>
              <a href="https://github.com/sandraschi/steam-mcp/blob/main/INSTALL.md" className="text-blue-400 underline">Installation</a>
              {" — "}all install methods, prerequisites
            </li>
            <li>
              <a href="https://github.com/sandraschi/steam-mcp/blob/main/docs/CONFIGURATION.md" className="text-blue-400 underline">Configuration</a>
              {" — "}env vars and Steam auth
            </li>
            <li>
              <a href="https://github.com/sandraschi/steam-mcp/blob/main/docs/TOOLS.md" className="text-blue-400 underline">Tool Reference</a>
              {" — "}full operation reference with examples
            </li>
            <li>
              <a href="https://github.com/sandraschi/mcp-central-docs/blob/main/docs/gamedev/STEAM_PUBLISHING.md" className="text-blue-400 underline">Steam Publishing</a>
              {" — "}Steamworks setup, Direct fee, credentials
            </li>
            <li>
              <a href="https://github.com/sandraschi/steam-mcp/blob/main/docs/DEVELOPMENT.md" className="text-blue-400 underline">Development</a>
              {" — "}contributing, local setup, standards
            </li>
            <li>
              <a href="https://github.com/sandraschi/steam-mcp/blob/main/docs/TROUBLESHOOTING.md" className="text-blue-400 underline">Troubleshooting</a>
              {" — "}common issues and fixes
            </li>
            <li>
              <a href="https://github.com/sandraschi/mcp-central-docs/blob/main/projects/steam-mcp/README.md" className="text-blue-400 underline">Fleet Project Page</a>
              {" — "}central docs overview
            </li>
          </ul>
        </section>
      </div>
    </div>
  );
}
