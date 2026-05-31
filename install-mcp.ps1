#!/usr/bin/env pwsh
# Install steam-mcp into an MCP client config.
# Usage: .\install-mcp.ps1 claude|cursor|windsurf|zed|antigravity|lmstudio|code|print
param([string]$Client = "print")

$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$ManifestPath = Join-Path $RepoRoot "manifest.json"

if (-not (Test-Path $ManifestPath)) {
    Write-Host "ERROR: manifest.json not found at $ManifestPath" -ForegroundColor Red
    exit 1
}

$mf = Get-Content $ManifestPath -Raw | ConvertFrom-Json
$Name = $mf.name
$Cmd = "uv"
$Args = @("run", "--directory", $RepoRoot, "steam-mcp")

$Entry = @{
    command = $Cmd
    args    = $Args
    env     = @{
        STEAM_API_KEY = ""
        STEAM_ID      = ""
        PYTHONUNBUFFERED = "1"
    }
}

$Block = @{ mcpServers = @{ $Name = $Entry } }
$Json = $Block | ConvertTo-Json -Depth 6

$Paths = @{
    claude      = @{ Path = "$env:APPDATA\Claude\claude_desktop_config.json"; Key = "mcpServers" }
    cursor      = @{ Path = "$env:APPDATA\Cursor\User\globalStorage\cursor-storage\mcp_config.json"; Key = "mcpServers" }
    windsurf    = @{ Path = "$env:USERPROFILE\.codeium\windsurf\mcp_config.json"; Key = "mcpServers" }
    zed         = @{ Path = "$env:APPDATA\Zed\settings.json"; Key = "mcpServers" }
    antigravity = @{ Path = "$env:USERPROFILE\.gemini\antigravity\mcp_config.json"; Key = "mcpServers" }
    lmstudio    = @{ Path = "$env:USERPROFILE\.lmstudio\mcp.json"; Key = "mcpServers" }
    code        = @{ Path = "$RepoRoot\.vscode\settings.json"; Key = "mcp" }
}

switch -Wildcard ($Client) {
    "print" {
        Write-Host $Json -ForegroundColor Cyan
        Write-Host "`nCopy this into your MCP client config. Set STEAM_API_KEY and STEAM_ID in env." -ForegroundColor Gray
    }
    default {
        $c = $Paths[$Client]
        if (-not $c) {
            Write-Host "Unknown client '$Client'. Use: claude, cursor, windsurf, zed, antigravity, lmstudio, code, print" -ForegroundColor Red
            exit 1
        }
        $cfgDir = Split-Path -Parent $c.Path
        if (-not (Test-Path $cfgDir)) { New-Item -ItemType Directory -Path $cfgDir -Force | Out-Null }
        $existing = @{}
        if (Test-Path $c.Path) {
            $raw = Get-Content $c.Path -Raw | ConvertFrom-Json
            $raw.PSObject.Properties | ForEach-Object { $existing[$_.Name] = $_.Value }
        }
        if (-not $existing.ContainsKey($c.Key)) { $existing[$c.Key] = @{} }
        if ($existing[$c.Key] -isnot [hashtable]) {
            $servers = @{}
            $existing[$c.Key].PSObject.Properties | ForEach-Object { $servers[$_.Name] = $_.Value }
            $existing[$c.Key] = $servers
        }
        $existing[$c.Key][$Name] = $Entry
        $existing | ConvertTo-Json -Depth 12 | Set-Content $c.Path -Encoding utf8
        Write-Host "Installed $Name into $($c.Path)" -ForegroundColor Green
    }
}
