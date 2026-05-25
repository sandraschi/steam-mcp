import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./e2e",
  timeout: 60000,
  retries: 1,
  use: {
    baseURL: "http://localhost:11021",
    headless: true,
    screenshot: "only-on-failure",
  },
  webServer: [
    {
      command: "uv run uvicorn steam_mcp.server:app --host 127.0.0.1 --port 11020 --log-level warning",
      port: 11020,
      cwd: "../",
      timeout: 30000,
      reuseExistingServer: false,
    },
    {
      command: "npx vite --port 11021 --host",
      port: 11021,
      cwd: ".",
      timeout: 30000,
      reuseExistingServer: false,
    },
  ],
});
