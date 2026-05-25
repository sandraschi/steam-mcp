import { test, expect } from "@playwright/test";

test.describe("Frontend", () => {
  test("Dashboard loads", async ({ page }) => {
    await page.goto("/");
    await expect(page.locator("text=Dashboard")).toBeVisible();
  });

  test("Topbar shows status indicators", async ({ page }) => {
    await page.goto("/");
    await expect(page.locator("text=Steam-MCP")).toBeVisible();
  });

  test("Settings page shows env info", async ({ page }) => {
    await page.goto("/settings");
    await expect(page.locator("text=STEAM_API_KEY")).toBeVisible();
  });

  test("Help page renders tool table", async ({ page }) => {
    await page.goto("/help");
    await expect(page.locator("text=Tools Overview")).toBeVisible();
  });

  test("Navigation sidebar links work", async ({ page }) => {
    await page.goto("/");
    await page.click("text=Help");
    await expect(page).toHaveURL(/\/help/);
  });
});

test.describe("REST API", () => {
  test("GET /api/status returns ok", async ({ request }) => {
    const resp = await request.get("/api/status");
    expect(resp.ok()).toBeTruthy();
    const body = await resp.json();
    expect(body.status).toBe("ok");
  });

  test("GET /api/tools returns tool list", async ({ request }) => {
    const resp = await request.get("/api/tools");
    expect(resp.ok()).toBeTruthy();
    const body = await resp.json();
    expect(body.tools.length).toBeGreaterThan(0);
  });
});
