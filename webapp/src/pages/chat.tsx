import { useState } from "react";
import { useQuery, useMutation } from "@tanstack/react-query";
import { apiPost, getTools, ToolInfo } from "@/lib/api";

type Mode = "ask" | "tool";

export default function Chat() {
  const { data: toolsData } = useQuery({ queryKey: ["tools"], queryFn: getTools });
  const tools = toolsData?.tools ?? [];
  const [mode, setMode] = useState<Mode>("ask");
  const [selected, setSelected] = useState("steam_store");
  const [argsJson, setArgsJson] = useState('{"operation": "search", "query": "Godot", "count": 5}');
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<{ role: "user" | "bot"; text: string }[]>([
    {
      role: "bot",
      text: "Ask in plain English (e.g. \"search for Godot\", \"players in TF2\", \"my library\") or switch to Tool mode.",
    },
  ]);

  const append = (role: "user" | "bot", text: string) =>
    setMessages((m) => [...m, { role, text }]);

  const ask = useMutation({
    mutationFn: (query: string) => apiPost<{ response: string }>("/chat", { query }),
    onSuccess: (data) => append("bot", data.response),
    onError: (e) => append("bot", String(e)),
  });

  const runTool = useMutation({
    mutationFn: async () => {
      const args = JSON.parse(argsJson);
      const res = await apiPost<{ success: boolean; data: { message?: string } }>(
        `/tools/${selected}/call`,
        { arguments: args },
      );
      return res.data?.message ?? JSON.stringify(res.data, null, 2);
    },
    onSuccess: (text) => {
      append("user", `${selected}(${argsJson})`);
      append("bot", text);
    },
    onError: (e) => append("bot", String(e)),
  });

  const onSubmit = () => {
    const q = input.trim();
    if (!q) return;
    append("user", q);
    setInput("");
    ask.mutate(q);
  };

  return (
    <div className="flex flex-col h-[calc(100vh-8rem)] gap-3">
      <div className="flex gap-2">
        <button
          type="button"
          className={`px-3 py-1 rounded text-sm ${mode === "ask" ? "bg-blue-600" : "bg-zinc-800"}`}
          onClick={() => setMode("ask")}
        >
          Ask Steam
        </button>
        <button
          type="button"
          className={`px-3 py-1 rounded text-sm ${mode === "tool" ? "bg-blue-600" : "bg-zinc-800"}`}
          onClick={() => setMode("tool")}
        >
          Tool console
        </button>
      </div>

      <div className="flex gap-4 flex-1 min-h-0">
        {mode === "tool" && (
          <aside className="w-56 shrink-0 border border-zinc-800 rounded-lg bg-zinc-900 p-2 overflow-y-auto">
            {tools.map((t: ToolInfo) => (
              <button
                key={t.name}
                type="button"
                onClick={() => setSelected(t.name)}
                className={`w-full text-left text-xs px-2 py-1.5 rounded ${selected === t.name ? "bg-blue-600 text-white" : "text-zinc-400 hover:bg-zinc-800"}`}
              >
                {t.name}
              </button>
            ))}
          </aside>
        )}

        <div className="flex-1 flex flex-col min-w-0">
          <div className="flex-1 overflow-y-auto border border-zinc-800 rounded-lg bg-zinc-950 p-4 space-y-3 mb-3">
            {messages.map((m, i) => (
              <div key={i} className={`text-sm ${m.role === "user" ? "text-blue-300" : "text-zinc-300"}`}>
                <span className="text-zinc-600 text-xs">{m.role === "user" ? "You" : "Steam-MCP"}</span>
                <pre className="whitespace-pre-wrap font-sans mt-1">{m.text}</pre>
              </div>
            ))}
          </div>

          {mode === "ask" ? (
            <div className="flex gap-2">
              <input
                className="flex-1 rounded border border-zinc-700 bg-zinc-900 px-3 py-2 text-sm"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && onSubmit()}
                placeholder='e.g. "search for Portal" or "players in 440"'
              />
              <button
                type="button"
                disabled={ask.isPending}
                onClick={onSubmit}
                className="rounded bg-blue-600 px-4 py-2 text-sm hover:bg-blue-500 disabled:opacity-50"
              >
                Send
              </button>
            </div>
          ) : (
            <>
              <textarea
                className="w-full h-24 rounded border border-zinc-700 bg-zinc-900 px-3 py-2 text-xs font-mono mb-2"
                value={argsJson}
                onChange={(e) => setArgsJson(e.target.value)}
              />
              <button
                type="button"
                disabled={runTool.isPending}
                onClick={() => runTool.mutate()}
                className="self-start rounded bg-blue-600 px-4 py-2 text-sm hover:bg-blue-500 disabled:opacity-50"
              >
                Run tool
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
