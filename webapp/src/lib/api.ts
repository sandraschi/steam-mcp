const API_ROOT = (import.meta.env.VITE_API_BASE as string | undefined)?.replace(/\/$/, "") ?? "";
const BASE = `${API_ROOT}/api`;

export interface ApiResponse<T = unknown> {
  success: boolean;
  message: string;
  data: T | null;
}

export interface StatusResponse {
  status: string;
  version: string;
  has_api_key: boolean;
  has_steam_id: boolean;
  tool_count?: number;
  tools?: string[];
  chat_mode?: string;
  llm_available?: boolean;
  capabilities?: {
    prefab: boolean;
    agentic: boolean;
    prompts: boolean;
    resources: boolean;
    skills?: boolean;
    llm_chat?: boolean;
  };
}

export interface ToolInfo {
  name: string;
  description: string;
  inputSchema: Record<string, unknown>;
}

export async function getStatus(): Promise<StatusResponse> {
  const res = await fetch(`${BASE}/status`);
  return res.json();
}

export async function getTools(): Promise<{ tools: ToolInfo[] }> {
  const res = await fetch(`${BASE}/tools`);
  return res.json();
}

export async function apiGet<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`);
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export async function apiPost<T>(path: string, body?: unknown): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export interface ToolResult {
  success: boolean;
  message?: string;
  data?: unknown;
}

export async function callTool(name: string, args: Record<string, unknown>): Promise<ToolResult> {
  const res = await apiPost<{ success: boolean; data: ToolResult }>(`/tools/${name}/call`, { arguments: args });
  return res.data as ToolResult;
}
