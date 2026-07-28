import { useMutation, useQuery } from "@tanstack/react-query";
import { useCallback, useEffect, useRef, useState } from "react";
import { apiPost, getTools, type ToolInfo } from "@/lib/api";
import { Bot, Download, Eraser, Loader2, Send, User } from "lucide-react";

const STORAGE_KEY = "steam-mcp-chat-history";
const PERSONALITY_KEY = "steam-mcp-chat-personality";

type Message = { role: "user" | "assistant"; content: string };
type Personality = { id: string; label: string; prompt: string };
type Mode = "ask" | "tool";

const PERSONALITIES: Personality[] = [
  { id: "gaming", label: "Gaming Expert", prompt: "You are a Steam and gaming expert. Help with game recommendations, library organization, and understanding Steam features." },
  { id: "deals", label: "Deal Hunter", prompt: "You are a deal-hunting specialist. Focus on finding discounts, price comparisons, bundle deals, and wishlist price tracking." },
  { id: "summarizer", label: "Quick Summarizer", prompt: "You are a concise assistant. Provide brief, focused answers with bullet points." },
  { id: "custom", label: "Custom", prompt: "" },
];

const EXAMPLE_GROUPS: Record<string, string[]> = {
  "Games": ["What are the most-played games on Steam right now?", "Search for strategy games with 'very positive' reviews", "Show achievements for a game"],
  "Store": ["Search for games like Portal on the Steam store", "What are the top-selling games this week?", "Find games on sale with discount >50%"],
  "Library": ["Show my recently played games", "How many games are in my library?", "Show my wishlist"],
};

function loadHistory(): Message[] {
  try { const raw = localStorage.getItem(STORAGE_KEY); return raw ? JSON.parse(raw) : []; } catch { return []; }
}

function saveHistory(messages: Message[]) {
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(messages.slice(-100))); } catch {}
}

function loadPersonality(): string {
  try { return localStorage.getItem(PERSONALITY_KEY) || "gaming"; } catch { return "gaming"; }
}

export default function Chat() {
  const { data: toolsData } = useQuery({ queryKey: ["tools"], queryFn: getTools });
  const tools = toolsData?.tools ?? [];
  const [messages, setMessages] = useState<Message[]>(loadHistory);
  const [mode, setMode] = useState<Mode>("ask");
  const [selected, setSelected] = useState("steam_store");
  const [argsJson, setArgsJson] = useState('{"operation": "search", "query": "Godot", "count": 5}');
  const [input, setInput] = useState("");
  const [personalityId, setPersonalityId] = useState(loadPersonality);
  const endRef = useRef<HTMLDivElement>(null);

  const personality = PERSONALITIES.find(p => p.id === personalityId) || PERSONALITIES[0];

  useEffect(() => { endRef.current?.scrollIntoView({ behavior: "smooth" }); }, [messages]);

  useEffect(() => { saveHistory(messages); }, [messages]);

  useEffect(() => { localStorage.setItem(PERSONALITY_KEY, personalityId); }, [personalityId]);

  const append = useCallback((role: "user" | "assistant", text: string) => {
    setMessages((prev) => [...prev, { role, content: text }]);
  }, []);

  const ask = useMutation({
    mutationFn: (query: string) => apiPost<{ response: string }>("/chat", { query }),
    onSuccess: (data) => append("assistant", data.response),
    onError: (e) => append("assistant", String(e)),
  });

  const runTool = useMutation({
    mutationFn: async () => {
      const args = JSON.parse(argsJson);
      const res = await apiPost<{ success: boolean; data: { message?: string } }>(`/tools/${selected}/call`, { arguments: args });
      return res.data?.message ?? JSON.stringify(res.data, null, 2);
    },
    onSuccess: (text) => {
      append("user", `${selected}(${argsJson})`);
      append("assistant", text);
    },
    onError: (e) => append("assistant", String(e)),
  });

  const onSubmit = useCallback(() => {
    const q = input.trim();
    if (!q) return;
    append("user", q);
    setInput("");
    ask.mutate(q);
  }, [input, ask, append]);

  const handleExport = useCallback(() => {
    const lines = messages.map(m => {
      const ts = new Date().toISOString();
      return `[${ts}] ${m.role === "user" ? "You" : "Assistant"}: ${m.content}`;
    }).join("\n");
    const blob = new Blob([lines], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url; a.download = `steam-mcp-chat-${Date.now()}.txt`; a.click();
    URL.revokeObjectURL(url);
  }, [messages]);

  const handleClear = useCallback(() => {
    setMessages([]);
    localStorage.removeItem(STORAGE_KEY);
  }, []);

  return (
    <div className="flex flex-col h-[calc(100vh-8rem)] gap-3" data-testid="chat-page">
      <div data-testid="chat-controls" className="flex items-center justify-between flex-wrap gap-2">
        <div className="flex gap-2">
          <button type="button" className={`px-3 py-1 rounded text-sm ${mode === "ask" ? "bg-blue-600" : "bg-zinc-800"}`} onClick={() => setMode("ask")}>Ask Steam</button>
          <button type="button" className={`px-3 py-1 rounded text-sm ${mode === "tool" ? "bg-blue-600" : "bg-zinc-800"}`} onClick={() => setMode("tool")}>Tool console</button>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs text-blue-400 bg-blue-950/30 px-2 py-0.5 rounded font-medium">skill:steam-expert</span>
          <select
            data-testid="personality-select"
            value={personalityId}
            onChange={e => setPersonalityId(e.target.value)}
            className="bg-zinc-800 text-zinc-100 border border-zinc-600 rounded px-2 py-1 text-xs"
          >
            {PERSONALITIES.map(p => <option key={p.id} value={p.id}>{p.label}</option>)}
          </select>
          <button onClick={handleExport} disabled={messages.length === 0} data-testid="chat-export" title="Export chat" className="p-1.5 rounded text-zinc-400 hover:text-white disabled:opacity-30">
            <Download className="w-4 h-4" />
          </button>
          <button onClick={handleClear} disabled={messages.length === 0} data-testid="chat-clear" title="Clear chat" className="p-1.5 rounded text-zinc-400 hover:text-white disabled:opacity-30">
            <Eraser className="w-4 h-4" />
          </button>
        </div>
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
          <div className="flex-1 overflow-y-auto border border-zinc-800 rounded-lg bg-zinc-950 p-4 space-y-3 mb-3" data-testid="chat-messages">
            {messages.length === 0 && (
              <div className="flex flex-col items-center justify-center h-full text-zinc-600 gap-2">
                <Bot className="w-8 h-8" />
                <p className="text-sm">Ask about Steam games, store, or your library.</p>
              </div>
            )}
            {messages.map((m, i) => (
              <div key={i} className={`flex gap-3 ${m.role === "assistant" ? "" : "flex-row-reverse"}`}>
                <div className={`h-7 w-7 rounded-full flex items-center justify-center border shrink-0 ${m.role === "assistant" ? "bg-blue-900/20 border-blue-800" : "bg-zinc-700 border-zinc-600"}`}>
                  {m.role === "assistant" ? <Bot className="h-3.5 w-3.5 text-blue-400" /> : <User className="h-3.5 w-3.5 text-zinc-300" />}
                </div>
                <div className={`flex-1 space-y-1 ${m.role === "assistant" ? "" : "text-right"}`}>
                  <span className={`text-xs ${m.role === "assistant" ? "text-blue-400" : "text-zinc-300"}`}>
                    {m.role === "assistant" ? "Steam-MCP" : "You"}
                  </span>
                  <div className={`text-sm p-3 rounded-md inline-block max-w-[80%] text-left whitespace-pre-wrap ${m.role === "assistant" ? "bg-blue-950/10 border border-blue-900/30 text-zinc-300" : "bg-zinc-900/50 border border-zinc-800 text-zinc-200"}`}>
                    {m.content}
                  </div>
                </div>
              </div>
            ))}
            {(ask.isPending || runTool.isPending) && (
              <div className="flex gap-3">
                <div className="h-7 w-7 rounded-full bg-blue-900/20 flex items-center justify-center border border-blue-800">
                  <Bot className="h-3.5 w-3.5 text-blue-400" />
                </div>
                <div className="flex items-center gap-2 text-sm text-zinc-500">
                  <Loader2 className="h-3.5 w-3.5 animate-spin" /> Processing...
                </div>
              </div>
            )}
            <div ref={endRef} />
          </div>

          <div className="flex flex-wrap gap-2 mb-2" data-testid="example-prompts">
            {Object.entries(EXAMPLE_GROUPS).map(([group, prompts]) => (
              <div key={group} className="flex items-center gap-1 flex-wrap">
                <span className="text-xs text-zinc-500 mr-1">{group}:</span>
                {prompts.map(p => (
                  <button
                    key={p}
                    onClick={() => mode === "ask" ? (setInput(p)) : setArgsJson(JSON.stringify({ operation: p.toLowerCase().replace(/\s+/g, "_") }))}
                    className="text-xs px-2.5 py-1 rounded-full border border-zinc-700 text-zinc-400 hover:bg-zinc-800 hover:text-zinc-200 transition-colors"
                  >
                    {p}
                  </button>
                ))}
              </div>
            ))}
          </div>

          {mode === "ask" ? (
            <div className="flex gap-2">
              <input
                data-testid="chat-input"
                className="flex-1 rounded border border-zinc-700 bg-zinc-900 px-3 py-2 text-sm text-white placeholder-zinc-500"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && onSubmit()}
                placeholder='e.g. "search for Portal" or "players in 440"'
              />
              <button
                type="button"
                disabled={ask.isPending || !input.trim()}
                onClick={onSubmit}
                className="rounded bg-blue-600 px-4 py-2 text-sm hover:bg-blue-500 disabled:opacity-50 flex items-center gap-1.5"
                data-testid="chat-send"
              >
                <Send className="w-4 h-4" /> Send
              </button>
            </div>
          ) : (
            <>
              <textarea
                className="w-full h-24 rounded border border-zinc-700 bg-zinc-900 px-3 py-2 text-xs font-mono mb-2 text-zinc-200"
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
