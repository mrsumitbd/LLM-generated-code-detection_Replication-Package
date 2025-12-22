from typing import List
from d365fo_client_manager import D365FOClientManager
from tool import Tool

class ConnectionTools:
    """Connection and testing tools for the MCP server."""

    def __init__(self, client_manager: D365FOClientManager):
        self._client_manager = client_manager

    def get_tools(self) -> List[Tool]:
        return [
            self._get_test_connection_tool(),
            self._get_environment_info_tool()
        ]

    def _get_test_connection_tool(self) -> Tool:
        return Tool(
            name="Test Connection",
            description="Checks the connection to the MCP server",
            action=self._client_manager.test_connection
        )

    def _get_environment_info_tool(self) -> Tool:
        return Tool(
            name="Environment Info",
            description="Retrieves information about the current environment",
            action=self._client_manager.get_environment_info
        )