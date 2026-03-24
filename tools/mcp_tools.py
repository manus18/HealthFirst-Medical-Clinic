import os
from dotenv import load_dotenv
load_dotenv()

from langchain_mcp_adapters.client import MultiServerMCPClient

COMPOSIO_API_KEY= os.getenv("COMPOSIO_API_KEY","")
COMPOSIO_URL= os.getenv("COMPOSIO_URL","")

def get_mcp_client():
    """
    Get MCP client for Composio MCP server
    """
    client = MultiServerMCPClient(
        {
            "composio": {
                "url": COMPOSIO_URL,
                "transport": "streamable_http",
                "headers": {
                    "x-api-key": COMPOSIO_API_KEY
                }
            }
        }
    )
    return client

async def get_calendar_tools(client: MultiServerMCPClient):
    """
    Get calendar tools from Composio MCP server
    """
    tools = await client.get_tools()
    return [t for t in tools if "calendar" in t.name.lower()]

async def get_gmail_tools(client: MultiServerMCPClient):
    """
    Get Gmail tools from Composio MCP server
    """
    tools = await client.get_tools()
    return [t for t in tools if "gmail" in t.name.lower()]