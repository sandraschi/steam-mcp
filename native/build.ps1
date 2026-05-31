#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Full release build: PyInstaller sidecar + Tauri Windows installer.
#>
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot

Write-Host "== steam-mcp Tauri Release Build ==" -ForegroundColor Cyan

Write-Host "-> [1/3] Building webapp..." -ForegroundColor Yellow
Push-Location "$Root\webapp"
try {
    npm install
    npm run build
} finally { Pop-Location }

Write-Host "-> [2/3] Building PyInstaller sidecar..." -ForegroundColor Yellow
pwsh -NoLogo -File "$Root\native\build-sidecar.ps1"

Write-Host "-> [3/3] Building Tauri app..." -ForegroundColor Yellow
Push-Location "$Root\native"
try {
    $env:Path = "$env:USERPROFILE\.cargo\bin;$env:Path"
    npm install
    npx @tauri-apps/cli build
} finally { Pop-Location }

$installer = "$Root\native\target\release\bundle\nsis\steam-mcp-native_0.3.0_x64-setup.exe"
Write-Host "== Build complete ==" -ForegroundColor Green
Write-Host "Installer: $installer" -ForegroundColor Cyan
