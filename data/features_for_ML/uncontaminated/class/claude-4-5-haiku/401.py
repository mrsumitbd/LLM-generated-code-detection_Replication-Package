import ctypes
import re
from ctypes import wintypes
import psutil

class PotPlayerIntegration:
    """
    Class for interacting with PotPlayer using Windows messaging API.
    Provides position and duration data for accurate scrobbling.
    """

    WM_COPYDATA = 0x004A
    POTPLAYER_COMMAND_GET_STATE = 10010
    POTPLAYER_COMMAND_GET_DURATION = 10011
    POTPLAYER_COMMAND_GET_POSITION = 10012
    POTPLAYER_COMMAND_GET_FILE_NAME = 10013

    def __init__(self):
        self.user32 = ctypes.windll.user32
        self.kernel32 = ctypes.windll.kernel32

    def get_position_duration(self, process_name=None):
        """
        Get current playback position and total duration in milliseconds.
        Returns tuple (position_ms, duration_ms) or (None, None) if not available.
        """
        try:
            hwnd = self._find_potplayer_window(process_name)
            if not hwnd:
                return None, None

            position = self._send_command(hwnd, self.POTPLAYER_COMMAND_GET_POSITION)
            duration = self._send_command(hwnd, self.POTPLAYER_COMMAND_GET_DURATION)

            if position is not None and duration is not None:
                return position, duration
            return None, None
        except Exception:
            return None, None

    def is_paused(self):
        """
        Check if PotPlayer is currently paused.
        Returns True if paused, False if playing, None if not available.
        """
        try:
            hwnd = self._find_potplayer_window()
            if not hwnd:
                return None

            state = self._send_command(hwnd, self.POTPLAYER_COMMAND_GET_STATE)
            if state is not None:
                return state == 0
            return None
        except Exception:
            return None

    def get_current_filepath(self, process_name=None):
        """
        Get the full file path of currently playing media.
        Returns filepath string or None if not available.
        """
        try:
            hwnd = self._find_potplayer_window(process_name)
            if not hwnd:
                return None

            filepath = self._get_file_path(hwnd)
            if filepath:
                return self._clean_filename(filepath)
            return None
        except Exception:
            return None

    def _is_menu_state(self, title):
        """
        Check if PotPlayer is in menu state based on window title.
        """
        if not title:
            return True
        menu_indicators = ["menu", "settings", "preferences", "about"]
        return any(indicator in title.lower() for indicator in menu_indicators)

    def _clean_filename(self, filename):
        """
        Clean and normalize filename by removing path and extension if needed.
        """
        if not filename:
            return None
        filename = filename.strip()
        if not filename:
            return None
        return filename

    def _find_potplayer_window(self, process_name=None):
        """
        Find PotPlayer window handle.
        """
        try:
            if process_name is None:
                process_name = "PotPlayer"

            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if process_name.lower() in proc.info['name'].lower():
                        hwnd = self.user32.FindWindowW(None, None)
                        while hwnd:
                            pid = wintypes.DWORD()
                            self.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
                            if pid.value == proc.info['pid']:
                                return hwnd
                            hwnd = self.user32.GetWindow(hwnd, 2)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            hwnd = self.user32.FindWindowW("PotPlayer MainFrame", None)
            if hwnd:
                return hwnd

            return None
        except Exception:
            return None

    def _send_command(self, hwnd, command):
        """
        Send command to PotPlayer and receive response.
        """
        try:
            result = self.user32.SendMessageW(hwnd, self.WM_COPYDATA, 0, command)
            if result:
                return result
            return None
        except Exception:
            return None

    def _get_file_path(self, hwnd):
        """
        Get current file path from PotPlayer.
        """
        try:
            class COPYDATASTRUCT(ctypes.Structure):
                _fields_ = [("dwData", wintypes.LPARAM),
                           ("cbData", wintypes.DWORD),
                           ("lpData", wintypes.LPVOID)]

            buffer = ctypes.create_unicode_buffer(260)
            cds = COPYDATASTRUCT()
            cds.dwData = self.POTPLAYER_COMMAND_GET_FILE_NAME
            cds.cbData = ctypes.sizeof(buffer)
            cds.lpData = ctypes.cast(buffer, wintypes.LPVOID)

            result = self.user32.SendMessageW(hwnd, self.WM_COPYDATA, 0, ctypes.byref(cds))
            if result:
                return buffer.value
            return None
        except Exception:
            return None