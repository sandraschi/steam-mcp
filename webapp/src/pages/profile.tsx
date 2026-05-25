import { useQuery } from "@tanstack/react-query";
import { apiGet } from "@/lib/api";

export default function Profile() {
  return (
    <div className="max-w-2xl">
      <h1 className="text-2xl font-bold mb-4">Profile</h1>
      <div className="rounded-lg border border-zinc-800 bg-zinc-900 p-6">
        <p className="text-sm text-zinc-400 mb-4">
          Your Steam profile data is available via the MCP tool <code className="text-blue-400">get_own_profile</code>.
          Connect your AI assistant to this MCP server to query profile details, friend lists, and achievements.
        </p>

        <h3 className="text-sm font-semibold text-zinc-300 mb-2">Available Profile Tools</h3>
        <ul className="text-sm text-zinc-500 space-y-1">
          <li><code className="text-blue-400">get_own_profile</code> — Your player summary</li>
          <li><code className="text-blue-400">get_player_summaries(steamids)</code> — Look up players</li>
          <li><code className="text-blue-400">get_friend_list(steamid)</code> — Get friends</li>
          <li><code className="text-blue-400">resolve_vanity_url(vanity_url)</code> — Resolve custom URL</li>
        </ul>
      </div>
    </div>
  );
}
