import platform
import re
import win32gui
import win32con
import psutil

class PotPlayerIntegration:
    """
    Class for interacting with PotPlayer using Windows messaging API.
    Provides position and duration data for accurate scrobbling.
    """
    
    def __init__(self):
        self.name = 'potplayer'
        self.platform = platform.system().lower()
        self.last_hwnd = None
        self.cached_filename = None
        self._connection_logged = False
        
        if self.platform == 'windows' and not all([win32gui, win32con, psutil]):
            logger.error("PotPlayer integration requires pywin32 and psutil libraries on Windows")

    def get_position_duration(self, process_name=None):
        """
        Get current playback position and duration from PotPlayer.
        
        Args:
            process_name: Optional process name for debugging
            
        Returns:
            tuple: (position, duration) in seconds, or (None, None) if unavailable
        """
        if self.platform != 'windows' or not all([win32gui, win32con]):
            return None, None
        
        hwnd = find_potplayer_hwnd()
        if not hwnd:
            self.last_hwnd = None
            self.cached_filename = None
            return None, None
        
        try:
            pos_ms = get_playback_ms(hwnd)
            total_ms = get_total_ms(hwnd)
            
            if pos_ms is None or total_ms is None or total_ms <= 0:
                return None, None
            
            position = pos_ms / 1000.0
            duration = total_ms / 1000.0
            
            if position < 0:
                position = 0.0
            elif position > duration:
                position = duration
            
            self.last_hwnd = hwnd
            
            if not self._connection_logged:
                logger.info("Successfully connected to PotPlayer via Windows messaging")
                self._connection_logged = True
            
            return round(position, 2), round(duration, 2)
            
        except Exception as e:
            logger.debug(f"Error getting position/duration from PotPlayer: {e}")
            return None, None

    def is_paused(self):
        """
        Check if PotPlayer playback is paused.
        
        Returns:
            bool: True if paused, False if playing, None if unknown
        """
        if self.platform != 'windows' or not win32gui:
            return None
            
        hwnd = find_potplayer_hwnd()
        if not hwnd:
            return None
            
        try:
            state = win32gui.SendMessage(hwnd, win32con.WM_USER, PPM_GET_PLAYBACK_STATUS, 0)
            return state != 2  # Not playing means paused or stopped
        except Exception as e:
            logger.debug(f"Error checking pause state: {e}")
            return None

    def get_current_filepath(self, process_name=None):
        """
        Get the filepath of the currently playing file in PotPlayer.
        
        Args:
            process_name: Optional process name for consistency with other integrations
            
        Returns:
            str: Filepath of the current media, or None if unavailable
        """
        if self.platform != 'windows' or not win32gui:
            return self.cached_filename
            
        hwnd = find_potplayer_hwnd()
        if not hwnd:
            return self.cached_filename
            
        try:
            window_title = win32gui.GetWindowText(hwnd)
            if not window_title or window_title == "PotPlayer":
                return self.cached_filename
            
            clean_title = window_title
            if " - PotPlayer" in clean_title:
                clean_title = clean_title.replace(" - PotPlayer", "").strip()
            
            if self._is_menu_state(clean_title):
                logger.debug(f"Detected menu state: '{clean_title}', using cached filename")
                return self.cached_filename
            
            cleaned_filename = self._clean_filename(clean_title)
            if cleaned_filename:
                self.cached_filename = cleaned_filename
                logger.debug(f"Cached valid filename from PotPlayer: '{cleaned_filename}'")
                return cleaned_filename
                
            return self.cached_filename
                
        except Exception as e:
            logger.debug(f"Error getting filepath from PotPlayer: {e}")
            return self.cached_filename

    def _is_menu_state(self, title):
        """Check if the title represents a menu/UI state rather than a filename."""
        if not title:
            return True
            
        menu_patterns = [
            r'^Chapter \d+',
            r'^Show main menu',
            r'^Open file',
            r'^Preferences',
            r'^Settings', 
            r'^\d{2}:\d{2}:\d{2}',
            r'Speed: \d+%',
            r'Volume: \d+%',
            r'Seeking to',
            r'Loading',
            r'Buffering',
        ]
        
        return any(re.match(pattern, title, re.IGNORECASE) for pattern in menu_patterns)

    def _clean_filename(self, filename):
        """Clean up filename by removing subtitle indicators and other appendages."""
        if not filename:
            return None
        
        cleaned = filename
        
        cleaned = re.sub(r'\s*\(With subtitles\)$', '', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r'\s*\[Subtitles.*?\]$', '', cleaned, flags=re.IGNORECASE)
        cleaned = cleaned.strip()
        
        if len(cleaned) < 3:
            return None
            
        if (any(ext in cleaned.lower() for ext in ['.mkv', '.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v'])
            or any(pattern in cleaned for pattern in ['1080p', '720p', '4K', '2160p', 'x264', 'x265', 'HEVC', 'BluRay', 'WEB-DL'])):
            return cleaned
            
        return None