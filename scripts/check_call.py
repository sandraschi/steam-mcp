import asyncio, sys

sys.path.insert(0, ".")

from steam_mcp.mcp.registry import mcp
from steam_mcp.mcp import tools  # noqa: F401


async def main():
    tool = await mcp.get_tool("get_app_details")
    print(f"Tool type: {type(tool).__name__}")
    print(f"Name: {tool.name}")
    print(f"Description: {tool.description}")
    print(f"inputSchema: {tool.inputSchema}")

    result = await mcp.call_tool("get_app_details", {"app_id": 440, "country": "US"})
    print(f"\nResult type: {type(result).__name__}")
    print(f"Result content: {result.content}")
    if hasattr(result, "isError"):
        print(f"isError: {result.isError}")
    import textwrap

    content_str = str(result.content)
    print(f"Content: {textwrap.shorten(content_str, 200)}")


asyncio.run(main())
