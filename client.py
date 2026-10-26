import asyncio
from pathlib import Path
from fastmcp import Client

client = Client(Path("main.py"))
# Path explicitly tells FastMCP main.py is a local server file, not a URL. This is important because FastMCP needs to know where to find the server code in order to connect to it.
# “My MCP client should connect to the FastMCP server defined in main.py.”

async def main():
    async with client:
        # print("Connected to the FastMCP server.")

        tools = await client.list_tools()
        resources = await client.list_resources()

        category_data = await client.read_resource(
            "categories://expense-categories"
        )

        print(category_data)

        for resource in resources:
            print(resource)
        # for tool in tools:
        #     print(tool.model_dump())
        #     print("-" *50)

        # result = await client.call_tool(
        #     "summarize",
        #     {
        #         "start_date": "2026-10-01",
        #         "end_date": "2026-10-31"
        #     }
        #  )
        # print(result)
        
asyncio.run(main())