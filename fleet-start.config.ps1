# Per-repo fleet start config for steam-mcp
# Edit ports/backend target here - start.ps1 is fleet-standard.
@{
    Name         = 'steam-mcp'
    BackendPort  = 11020
    FrontendPort = 11021
    HealthPath   = '/health'
    WebRoot      = 'D:\Dev\repos\steam-mcp\webapp'
    Backend = @{
        Kind          = 'uvicorn'
        UvicornTarget = 'steam_mcp.server:app'
        SyncExtras    = @('dev')
        Env           = @{ WEB_PORT = '11020' }
    }
    Frontend = @{
        Kind           = 'vite-npm'
        PackageManager = 'npm'
        PortEnvVar     = 'VITE_PORT'
        ApiTargetEnv   = 'VITE_API_TARGET'
    }
}
