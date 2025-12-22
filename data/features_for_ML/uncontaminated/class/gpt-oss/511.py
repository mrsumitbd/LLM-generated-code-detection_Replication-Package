from typing import List
import subprocess
from langchain.tools import StructuredTool


class AndroidTool:
    def __init__(self):
        pass

    def get_tools(self) -> List[StructuredTool]:
        def list_installed_packages() -> str:
            """Return a list of installed package names on the connected Android device."""
            try:
                result = subprocess.run(
                    ["adb", "shell", "pm", "list", "packages"],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                packages = [
                    line.replace("package:", "").strip()
                    for line in result.stdout.splitlines()
                    if line.startswith("package:")
                ]
                return "\n".join(packages)
            except subprocess.CalledProcessError as e:
                return f"Error listing packages: {e.stderr.strip()}"

        def get_device_info() -> str:
            """Return basic device information such as model, brand, and Android version."""
            try:
                result = subprocess.run(
                    ["adb", "shell", "getprop"],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                return result.stdout.strip()
            except subprocess.CalledProcessError as e:
                return f"Error getting device info: {e.stderr.strip()}"

        tools = [
            StructuredTool.from_function(
                func=list_installed_packages,
                name="list_installed_packages",
                description="List all installed package names on the connected Android device.",
            ),
            StructuredTool.from_function(
                func=get_device_info,
                name="get_device_info",
                description="Retrieve basic device information such as model, brand, and Android version.",
            ),
        ]
        return tools