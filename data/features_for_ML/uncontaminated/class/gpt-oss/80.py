from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, List

# Minimal Tool implementation – used if no external Tool is available.
@dataclass
class Tool:
    """Simple tool representation."""
    name: str
    description: str
    action: Callable[[], Any]

    def run(self) -> Any:
        """Execute the tool's action."""
        return self.action()


class ConnectionTools:
    """Connection and testing tools for the MCP server."""

    def __init__(self, client_manager: Any):
        """
        Initialize with a client manager that provides connection
        and environment information.

        Parameters
        ----------
        client_manager : Any
            An object that exposes methods for testing connections
            and retrieving environment information.
        """
        self.client_manager = client_manager

    def get_tools(self) -> List[Tool]:
        """
        Return a list of available tools.

        Returns
        -------
        List[Tool]
            A list containing the test connection tool and the
            environment information tool.
        """
        return [
            self._get_test_connection_tool(),
            self._get_environment_info_tool(),
        ]

    def _get_test_connection_tool(self) -> Tool:
        """
        Create a tool that tests the connection to the MCP server.

        Returns
        -------
        Tool
            A tool configured to test the connection.
        """
        # Attempt to use a dedicated test_connection method if available.
        test_action: Callable[[], Any]
        if hasattr(self.client_manager, "test_connection"):
            test_action = self.client_manager.test_connection
        else:
            # Fallback: try to perform a simple request or ping.
            def test_action() -> Any:
                try:
                    # Assume the client manager has a `connection` attribute
                    # that can be used to send a lightweight request.
                    conn = getattr(self.client_manager, "connection", None)
                    if conn is None:
                        raise RuntimeError("No connection attribute available.")
                    # Example: send a HEAD request or similar.
                    return conn.head("/")  # type: ignore
                except Exception as exc:
                    return f"Connection test failed: {exc}"

        return Tool(
            name="Test Connection",
            description="Test the connection to the MCP server.",
            action=test_action,
        )

    def _get_environment_info_tool(self) -> Tool:
        """
        Create a tool that retrieves environment information.

        Returns
        -------
        Tool
            A tool configured to fetch environment details.
        """
        # Attempt to use a dedicated get_environment_info method if available.
        env_action: Callable[[], Any]
        if hasattr(self.client_manager, "get_environment_info"):
            env_action = self.client_manager.get_environment_info
        else:
            # Fallback: try to access a property or method that returns info.
            def env_action() -> Any:
                try:
                    return getattr(self.client_manager, "environment_info", {})
                except Exception as exc:
                    return f"Failed to retrieve environment info: {exc}"

        return Tool(
            name="Environment Info",
            description="Retrieve environment information from the MCP server.",
            action=env_action,
        )