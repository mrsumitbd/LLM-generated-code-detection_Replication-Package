import sys, time, threading, logging, traceback
import webview, platform, subprocess
from config import Config
from variables import StaticVariables, Variables

class UIBase:
    def __init__(self, ui_path):
        self.next_logic_thread = None
        self.window = None
        self.html = open(ui_path, "r", encoding="utf-8").read()
    
    # api functions #
    def resize_window(self, width, height, device_pixel_ratio=None):
        if device_pixel_ratio is not None and current_os == "Windows":
            width, height = int(width * device_pixel_ratio), int(height * device_pixel_ratio)
            logging.info(f"Resizing window: ({width}, {height}) | Scale: {device_pixel_ratio}")
        
        else:
            width, height = int(width), int(height)
            logging.info(f"Resizing window: ({width}, {height})")

        self.window.resize(width, height)
        return "Done"

    def get_macro_information(self):
        return f"{Variables.session_id} | {Variables.current_version} ({Variables.current_branch})"
    
    def get_scale_override(self):
        return Config.UI_SCALE_OVERRIDE
    
    # window functions #
    def stop_window(self):
        if self.window: self.window.destroy()
        logging.info("[UIBase] Window destroyed successfully.")

    def create_window(self):
        logging.debug("Fetching 'UI_ON_TOP' configuration...")
        is_on_top = True
        if hasattr(Config, "UI_ON_TOP"):
            if isinstance(Config.UI_ON_TOP, bool):
                is_on_top = Config.UI_ON_TOP

        logging.debug(f"Creating a new pywebview window - on_top={is_on_top}...")
        self.window = webview.create_window(
            "mstudio45's DIG macro",
            html=self.html,
            
            width=672, height=101,

            frameless=True, easy_drag=False,
            transparent=False, shadow=True,
            on_top=is_on_top, focus=True
        )
        self.window.expose(self.resize_window, self.get_macro_information, self.get_scale_override)
        logging.debug("Window has been created.")