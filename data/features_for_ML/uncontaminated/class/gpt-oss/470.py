import tkinter as tk
import os
import json

class UIBase:
    def __init__(self, ui_path):
        """
        Initialize the UIBase with a path to a UI definition file.
        """
        self.ui_path = ui_path
        self.window = None
        self.scale_override = None
        self.macro_info = None

    def resize_window(self, width, height, device_pixel_ratio=None):
        """
        Resize the window to the specified width and height.
        If device_pixel_ratio is provided, adjust the size accordingly.
        """
        if not self.window:
            raise RuntimeError("Window has not been created yet.")
        if device_pixel_ratio:
            width = int(width * device_pixel_ratio)
            height = int(height * device_pixel_ratio)
        self.window.geometry(f"{width}x{height}")

    def get_macro_information(self):
        """
        Return macro information parsed from the UI file.
        The UI file is expected to be a JSON file containing a 'macros' key.
        """
        if self.macro_info is not None:
            return self.macro_info
        if not os.path.exists(self.ui_path):
            raise FileNotFoundError(f"UI file not found: {self.ui_path}")
        with open(self.ui_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.macro_info = data.get("macros", {})
        return self.macro_info

    def get_scale_override(self):
        """
        Return the scale override value if set, otherwise None.
        """
        return self.scale_override

    def stop_window(self):
        """
        Destroy the window and clean up resources.
        """
        if self.window:
            self.window.destroy()
            self.window = None

    def create_window(self):
        """
        Create a new Tkinter window based on the UI file.
        """
        if self.window:
            raise RuntimeError("Window already created.")
        self.window = tk.Tk()
        title = os.path.splitext(os.path.basename(self.ui_path))[0]
        self.window.title(title)
        # Load UI layout if needed (placeholder)
        # For example, set a default size
        self.window.geometry("800x600")
        return self.window