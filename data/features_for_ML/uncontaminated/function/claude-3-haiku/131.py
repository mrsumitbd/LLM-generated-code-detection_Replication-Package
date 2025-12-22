import os
import subprocess
import sys

def mcp_client_command():
    """
    MCP client commands.
    """
    if len(sys.argv) < 2:
        print("Usage: python script.py <command>")
        return

    command = sys.argv[1]

    if command == "start":
        start_mcp_client()
    elif command == "stop":
        stop_mcp_client()
    elif command == "restart":
        restart_mcp_client()
    else:
        print(f"Invalid command: {command}")

def start_mcp_client():
    """Start the MCP client."""
    try:
        subprocess.run(["mcp_client", "start"], check=True)
        print("MCP client started.")
    except subprocess.CalledProcessError as e:
        print(f"Error starting MCP client: {e}")

def stop_mcp_client():
    """Stop the MCP client."""
    try:
        subprocess.run(["mcp_client", "stop"], check=True)
        print("MCP client stopped.")
    except subprocess.CalledProcessError as e:
        print(f"Error stopping MCP client: {e}")

def restart_mcp_client():
    """Restart the MCP client."""
    stop_mcp_client()
    start_mcp_client()