import os
from dotenv import load_dotenv
from groq import Groq
from fastmcp import Client
from pathlib import Path
import json

load_dotenv()

groq = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

mcp_client = Client(Path("main.py"))

async def main():
    async with mcp_client:

        prompt_file = Path("resources/prompts/expense_prompt.txt")
        with open(prompt_file, "r") as file:
            system_prompt = file.read()

        
        tools = await mcp_client.list_tools()

        category_resource = await mcp_client.read_resource(
            "categories://expense-categories"
        )
        categories = category_resource[0].text

        # print("Categories loaded from MCP resource.")

        groq_tools = []

        for tool in tools:
            groq_tools.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.input_schema
                }
            })

        # print(groq_tools)
        user_message = input("You: ")

        response = groq.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": f"""
        Available categories:
        {categories}

        User request:
        {user_message}
        """
            }
        ],
            tools=groq_tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        if message.tool_calls:
            tool_call = message.tool_calls[0]

            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            # print("Tool selected:", tool_name)
            # print("Arguments:", arguments)

            result = await mcp_client.call_tool(
                tool_name,
                arguments
            )

            # print("MCP result:", result)

            if result.data is not None:
                tool_result = result.data
            elif result.content:
                tool_result = result.content[0].text
            else:
                tool_result = "No results returned from the tool."

            final_response = groq.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": f"""
        Available categories:
        {categories}

        Original user request:
        {user_message}
        """
                    },
                    {
                        "role": "assistant",
                        "tool_calls": message.tool_calls
                    },
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(tool_result)
                    }
                ],
                tools=groq_tools,
                tool_choice="none"
            )

            print("Final response:")
            print(final_response.choices[0].message.content)

        else:
            print("Groq did not select a tool.")
            print("Groq response:")
            print(message.content)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())