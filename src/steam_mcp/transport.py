import argparse
import sys

from fastmcp import FastMCP

from .config import settings


def run_server(mcp_instance: FastMCP, server_name: str = "steam-mcp") -> None:
    parser = argparse.ArgumentParser(description=f"Run {server_name}")
    parser.add_argument("--http", action="store_true", help="Run as HTTP SSE server")
    parser.add_argument("--port", type=int, default=settings.backend_port, help="HTTP port")
    parser.add_argument("--host", type=str, default=settings.host, help="Bind address")
    args = parser.parse_args()

    if args.http:
        mcp_instance.run(transport="sse", host=args.host, port=args.port)
    else:
        print(f"Starting {server_name} via STDIO...", file=sys.stderr)
        mcp_instance.run(transport="stdio")
