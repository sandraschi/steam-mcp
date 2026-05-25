import asyncio, sys

sys.path.insert(0, ".")

from steam_mcp.mcp.registry import mcp
from steam_mcp.mcp import tools  # noqa: F401


async def main():
    tl = await mcp.list_tools()
    t = tl[0]
    print(f"Name: {t.name}")
    print(f"Type: {type(t).__name__}")
    print(f"Description: {t.description}")
    attrs = [a for a in dir(t) if not a.startswith("_")]
    print(f"Attrs: {attrs}")


asyncio.run(main())
