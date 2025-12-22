from typing import List
from langchain.tools import StructuredTool
from langchain.tools import tool
import subprocess
import json
import re


class AndroidTool:

    def __init__(self):
        pass

    def get_tools(self) -> List[StructuredTool]:
        tools = [
            StructuredTool.from_function(
                func=self.list_devices,
                name="list_android_devices",
                description="List all connected Android devices via ADB"
            ),
            StructuredTool.from_function(
                func=self.get_device_info,
                name="get_android_device_info",
                description="Get information about a specific Android device",
                args_schema=self._get_device_info_schema()
            ),
            StructuredTool.from_function(
                func=self.install_app,
                name="install_android_app",
                description="Install an APK on an Android device",
                args_schema=self._install_app_schema()
            ),
            StructuredTool.from_function(
                func=self.uninstall_app,
                name="uninstall_android_app",
                description="Uninstall an app from an Android device",
                args_schema=self._uninstall_app_schema()
            ),
            StructuredTool.from_function(
                func=self.list_installed_apps,
                name="list_installed_apps",
                description="List all installed apps on an Android device",
                args_schema=self._list_installed_apps_schema()
            ),
            StructuredTool.from_function(
                func=self.execute_shell_command,
                name="execute_adb_shell_command",
                description="Execute a shell command on an Android device",
                args_schema=self._execute_shell_command_schema()
            ),
            StructuredTool.from_function(
                func=self.take_screenshot,
                name="take_android_screenshot",
                description="Take a screenshot from an Android device",
                args_schema=self._take_screenshot_schema()
            ),
            StructuredTool.from_function(
                func=self.get_logcat,
                name="get_android_logcat",
                description="Get logcat output from an Android device",
                args_schema=self._get_logcat_schema()
            ),
        ]
        return tools

    def list_devices(self) -> str:
        try:
            result = subprocess.run(
                ["adb", "devices"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.stdout
        except Exception as e:
            return f"Error listing devices: {str(e)}"

    def get_device_info(self, device_id: str) -> str:
        try:
            result = subprocess.run(
                ["adb", "-s", device_id, "shell", "getprop"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.stdout
        except Exception as e:
            return f"Error getting device info: {str(e)}"

    def install_app(self, device_id: str, apk_path: str) -> str:
        try:
            result = subprocess.run(
                ["adb", "-s", device_id, "install", apk_path],
                capture_output=True,
                text=True,
                timeout=60
            )
            return result.stdout + result.stderr
        except Exception as e:
            return f"Error installing app: {str(e)}"

    def uninstall_app(self, device_id: str, package_name: str) -> str:
        try:
            result = subprocess.run(
                ["adb", "-s", device_id, "uninstall", package_name],
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.stdout + result.stderr
        except Exception as e:
            return f"Error uninstalling app: {str(e)}"

    def list_installed_apps(self, device_id: str) -> str:
        try:
            result = subprocess.run(
                ["adb", "-s", device_id, "shell", "pm", "list", "packages"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.stdout
        except Exception as e:
            return f"Error listing installed apps: {str(e)}"

    def execute_shell_command(self, device_id: str, command: str) -> str:
        try:
            result = subprocess.run(
                ["adb", "-s", device_id, "shell", command],
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.stdout + result.stderr
        except Exception as e:
            return f"Error executing command: {str(e)}"

    def take_screenshot(self, device_id: str, output_path: str = "/sdcard/screenshot.png") -> str:
        try:
            subprocess.run(
                ["adb", "-s", device_id, "shell", "screencap", "-p", output_path],
                capture_output=True,
                text=True,
                timeout=10
            )
            return f"Screenshot saved to {output_path} on device"
        except Exception as e:
            return f"Error taking screenshot: {str(e)}"

    def get_logcat(self, device_id: str, lines: int = 100) -> str:
        try:
            result = subprocess.run(
                ["adb", "-s", device_id, "logcat", "-d"],
                capture_output=True,
                text=True,
                timeout=10
            )
            output_lines = result.stdout.split('\n')
            return '\n'.join(output_lines[-lines:])
        except Exception as e:
            return f"Error getting logcat: {str(e)}"

    def _get_device_info_schema(self):
        from pydantic import BaseModel, Field
        
        class GetDeviceInfoInput(BaseModel):
            device_id: str = Field(description="The device ID or serial number")
        
        return GetDeviceInfoInput

    def _install_app_schema(self):
        from pydantic import BaseModel, Field
        
        class InstallAppInput(BaseModel):
            device_id: str = Field(description="The device ID or serial number")
            apk_path: str = Field(description="Path to the APK file")
        
        return InstallAppInput

    def _uninstall_app_schema(self):
        from pydantic import BaseModel, Field
        
        class UninstallAppInput(BaseModel):
            device_id: str = Field(description="The device ID or serial number")
            package_name: str = Field(description="Package name of the app to uninstall")
        
        return UninstallAppInput

    def _list_installed_apps_schema(self):
        from pydantic import BaseModel, Field
        
        class ListInstalledAppsInput(BaseModel):
            device_id: str = Field(description="The device ID or serial number")
        
        return ListInstalledAppsInput

    def _execute_shell_command_schema(self):
        from pydantic import BaseModel, Field
        
        class ExecuteShellCommandInput(BaseModel):
            device_id: str = Field(description="The device ID or serial number")
            command: str = Field(description="Shell command to execute")
        
        return ExecuteShellCommandInput

    def _take_screenshot_schema(self):
        from pydantic import BaseModel, Field
        
        class TakeScreenshotInput(BaseModel):
            device_id: str = Field(description="The device ID or serial number")
            output_path: str = Field(default="/sdcard/screenshot.png", description="Output path on device")
        
        return TakeScreenshotInput

    def _get_logcat_schema(self):
        from pydantic import BaseModel, Field
        
        class GetLogcatInput(BaseModel):
            device_id: str = Field(description="The device ID or serial number")
            lines: int = Field(default=100, description="Number of log lines to retrieve")
        
        return GetLogcatInput