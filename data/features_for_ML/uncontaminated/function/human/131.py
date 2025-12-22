from nat.runtime.loader import PluginTypes
import click
from nat.runtime.loader import discover_and_register_plugins

def mcp_client_command():
    """
    MCP client commands.
    """
    try:
        from nat.runtime.loader import PluginTypes
        from nat.runtime.loader import discover_and_register_plugins
        discover_and_register_plugins(PluginTypes.CONFIG_OBJECT)
    except ImportError:
        click.echo("[WARNING] MCP client functionality requires nvidia-nat-mcp package.", err=True)
        pass