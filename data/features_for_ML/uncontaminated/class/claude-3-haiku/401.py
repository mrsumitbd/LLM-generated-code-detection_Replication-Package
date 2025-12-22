import win32api
import win32con
import win32gui
import os
import re

class PotPlayerIntegration:
    """
    Class for interacting with PotPlayer using Windows messaging API.
    Provides position and duration data for accurate scrobbling.
    """

    def __init__(self):
        self.hwnd = None

    def get_position_duration(self, process_name=None):
        if not self.hwnd:
            self.hwnd = self._get_window_handle(process_name)
        if self.hwnd:
            position = self._get_position()
            duration = self._get_duration()
            return position, duration
        return None, None

    def is_paused(self):
        if not self.hwnd:
            self.hwnd = self._get_window_handle()
        if self.hwnd:
            return self._is_paused()
        return None

    def get_current_filepath(self, process_name=None):
        if not self.hwnd:
            self.hwnd = self._get_window_handle(process_name)
        if self.hwnd:
            filepath = self._get_current_filepath()
            return self._clean_filename(filepath)
        return None

    def _is_menu_state(self, title):
        return bool(re.search(r'Menu|Options|Preferences', title, re.IGNORECASE))

    def _clean_filename(self, filename):
        return os.path.basename(filename)

    def _get_window_handle(self, process_name=None):
        if process_name:
            hwnd = win32gui.FindWindow(None, process_name)
        else:
            hwnd = win32gui.FindWindow(None, "PotPlayer")
        return hwnd

    def _get_position(self):
        position = win32api.SendMessage(self.hwnd, win32con.WM_USER, 0x400, 0x4E20)
        return position

    def _get_duration(self):
        duration = win32api.SendMessage(self.hwnd, win32con.WM_USER, 0x400, 0x4E21)
        return duration

    def _is_paused(self):
        state = win32api.SendMessage(self.hwnd, win32con.WM_USER, 0x400, 0x4E22)
        return state == 2