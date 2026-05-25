param(
    [switch]$Headless,
    [switch]$BackendOnly,
    [switch]$FrontendOnly,
    [switch]$NoBrowser
)

$ErrorActionPreference = "Stop"
$ScriptRoot = Split-Path -Parent $PSCommandPath
$BackendPort = 11020
$FrontendPort = 11021

Write-Host "=== Steam-MCP Launcher ===" -ForegroundColor Cyan

# Kill stale processes on our ports
foreach ($port in @($BackendPort, $FrontendPort)) {
    Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue | ForEach-Object {
        Write-Host "Killing stale process $($_.OwningProcess) on port $port" -ForegroundColor Yellow
        Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue
    }
}

if (-not $FrontendOnly) {
    Write-Host "Starting backend on port $BackendPort..." -ForegroundColor Green
    $backendJob = Start-Job -Name "steam-mcp-backend" -ScriptBlock {
        param($Root, $Port)
        Set-Location $Root
        uv run uvicorn steam_mcp.server:app --host 127.0.0.1 --port $Port --log-level warning
    } -ArgumentList $ScriptRoot, $BackendPort

    # Wait for backend readiness
    Write-Host "Waiting for backend..." -ForegroundColor Yellow
    $ready = $false
    for ($i = 0; $i -lt 30; $i++) {
        try {
            $r = Invoke-WebRequest -Uri "http://127.0.0.1:$BackendPort/api/status" -TimeoutSec 2 -UseBasicParsing -ErrorAction SilentlyContinue
            if ($r.StatusCode -eq 200) { $ready = $true; break }
        } catch {}
        Start-Sleep 1
    }
    if (-not $ready) { Write-Host "Backend failed to start" -ForegroundColor Red; exit 1 }
    Write-Host "Backend ready on port $BackendPort" -ForegroundColor Green
}

if (-not $BackendOnly) {
    Write-Host "Starting frontend on port $FrontendPort..." -ForegroundColor Green
    $WebRoot = Join-Path $ScriptRoot "webapp"
    $frontendProc = Start-Process -NoNewWindow -FilePath "npx" -ArgumentList "vite --port $FrontendPort --host" -WorkingDirectory $WebRoot -PassThru

    # Wait for frontend
    Write-Host "Waiting for frontend..." -ForegroundColor Yellow
    $ready = $false
    for ($i = 0; $i -lt 60; $i++) {
        try {
            $r = Invoke-WebRequest -Uri "http://127.0.0.1:$FrontendPort" -TimeoutSec 2 -UseBasicParsing -ErrorAction SilentlyContinue
            if ($r.StatusCode -eq 200) { $ready = $true; break }
        } catch {}
        Start-Sleep 1
    }
    if (-not $ready) { Write-Host "Frontend failed to start" -ForegroundColor Red; exit 1 }
    Write-Host "Frontend ready on port $FrontendPort" -ForegroundColor Green

    if (-not $NoBrowser) {
        Start-Process "http://127.0.0.1:$FrontendPort"
    }
}

Write-Host "=== Steam-MCP is running ===" -ForegroundColor Cyan
Write-Host "  Backend:  http://127.0.0.1:$BackendPort" -ForegroundColor Cyan
Write-Host "  Frontend: http://127.0.0.1:$FrontendPort" -ForegroundColor Cyan
Write-Host "  MCP:      http://127.0.0.1:$BackendPort/mcp" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop" -ForegroundColor Gray

# Keep alive
try {
    while ($true) {
        if ($backendJob -and $backendJob.State -in @("Completed", "Failed")) {
            Write-Host "Backend stopped: $($backendJob.State)" -ForegroundColor Red
            Receive-Job $backendJob
            break
        }
        Start-Sleep 2
    }
} finally {
    Write-Host "Shutting down..." -ForegroundColor Yellow
    if ($backendJob) { Stop-Job $backendJob -ErrorAction SilentlyContinue; Remove-Job $backendJob -ErrorAction SilentlyContinue }
    if ($frontendProc -and -not $frontendProc.HasExited) { Stop-Process -Id $frontendProc.Id -Force -ErrorAction SilentlyContinue }
}
