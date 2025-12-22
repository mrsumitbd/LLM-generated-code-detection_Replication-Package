from typing import List, Any
from mcp.types import Tool, TextContent
from pydantic import BaseModel, Field
import json


class ConnectionTools:
    """Connection and testing tools for the MCP server."""

    def __init__(self, client_manager: D365FOClientManager):
        self.client_manager = client_manager

    def get_tools(self) -> List[Tool]:
        return [
            self._get_test_connection_tool(),
            self._get_environment_info_tool(),
        ]

    def _get_test_connection_tool(self) -> Tool:
        return Tool(
            name="test_connection",
            description="Test the connection to the D365 Finance and Operations environment",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        )

    def _get_environment_info_tool(self) -> Tool:
        return Tool(
            name="get_environment_info",
            description="Get information about the connected D365 Finance and Operations environment",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        )