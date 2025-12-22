import ctypes
import ctypes.wintypes as wintypes
import os
import psutil

# Constants
WM_USER = 0x0400
# PotPlayer message offsets (verified from documentation)
PP_GET_POSITION = WM_USER + 0x1000
PP_GET_DURATION = WM_USER + 0x1001
PP_GET_FILENAME = WM_USER + 0x1002
PP_GET_PLAY_STATE = WM_USER + 0x1003

# Windows API
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

EnumWindowsProc = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HWND,
    wintypes.LPARAM
)

class PotPlayerIntegration:
    """
    Class for interacting with PotPlayer using Windows messaging API.
    Provides position and duration data for accurate scrobbling.
    """

    def __init__(self):
        # Cache for window handle to avoid repeated enumeration
        self._hwnd_cache = {}

    def _find_window(self, process_name=None):
        """
        Find the main window handle of PotPlayer.
        If process_name is provided, only windows belonging to that process are considered.
        """
        hwnd = None

        def callback(hWnd, lParam):
            nonlocal hwnd
            # Skip invisible windows
            if not user32.IsWindowVisible(hWnd):
                return True
            # Get window title
            length = user32.GetWindowTextLengthW(hWnd)
            title_buf = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hWnd, title_buf, length + 1)
            title = title_buf.value
            # Basic check for PotPlayer window class or title
            if "PotPlayer" not in title:
                return True
            # If process_name is specified, verify process id
            if process_name:
                pid = wintypes.DWORD()
                user32.GetWindowThreadProcessId(hWnd, ctypes.byref(pid))
                try:
                    proc = psutil.Process(pid.value)
                    if proc.name().lower() != process_name.lower():
                        return True
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    return True
            hwnd = hWnd
            return False  # stop enumeration

        user32.EnumWindows(EnumWindowsProc(callback), 0)
        return hwnd

    def get_position_duration(self, process_name=None):
        """
        Returns a tuple (position_ms, duration_ms) for the current PotPlayer instance.
        If the window is not found, returns (None, None).
        """
        hwnd = self._find_window(process_name)
        if not hwnd:
            return None, None

        # Position
        pos = user32.SendMessageW(hwnd, PP_GET_POSITION, 0, 0)
        # Duration
        dur = user32.SendMessageW(hwnd, PP_GET_DURATION, 0, 0)
        return pos, dur

    def is_paused(self):
        """
        Returns True if PotPlayer is paused, False if playing.
        """
        hwnd = self._find_window()
        if not hwnd:
            return None
        state = user32.SendMessageW(hwnd, PP_GET_PLAY_STATE, 0, 0)
        # According to docs: 0 = paused, 1 = playing
        return state == 0

    def get_current_filepath(self, process_name=None):
        """
        Returns the full path of the currently playing file.
        If the window is not found or no file is loaded, returns None.
        """
        hwnd = self._find_window(process_name)
        if not hwnd:
            return None

        # Prepare buffer for filename
        buf_len = 260  # MAX_PATH
        buffer = ctypes.create_unicode_buffer(buf_len)
        # Send message; lParam points to buffer
        user32.SendMessageW(hwnd, PP_GET_FILENAME, buf_len, ctypes.byref(buffer))
        filename = buffer.value
        if not filename:
            return None
        return filename

    def _is_menu_state(self, title):
        """
        Detects if the PotPlayer window is in a menu state based on its title.
        """
        # Common menu titles contain 'Menu' or 'Open'
        return "Menu" in title or "Open" in title

    def _clean_filename(self, filename):
        """
        Cleans a filename string: removes path, extension, replaces underscores,
        and strips surrounding whitespace.
        """
        if not filename:
            return None
        base = os.path.basename(filename)
        name, _ = os.path.splitext(base)
        # Replace underscores and hyphens with spaces
        cleaned = name.replace('_', ' ').replace('-', ' ')
        return cleaned.strip()