import asyncio

class MusicPlayer:
    def __init__(self):
        self.voice_client = None
        self.current_task = None
        self.queue = asyncio.Queue()
        self.history = []
        self.radio_playlist = [] 
        self.current_url = None
        self.current_info = None
        self.text_channel = None
        self.loop_current = False
        self.autoplay_enabled = False
        self.last_was_single = False
        self.start_time = 0
        self.playback_started_at = None
        self.active_filter = None
        self.seek_info = None

        # --- Attributes for lyrics, karaoke, and filters ---
        self.lyrics_task = None
        self.lyrics_message = None
        self.synced_lyrics = None
        self.is_seeking = False
        self.playback_speed = 1.0
        
        self.is_reconnecting = False 
        self.is_current_live = False

        self.hydration_task = None
        self.hydration_lock = asyncio.Lock()
        
        self.suppress_next_now_playing = False

        self.is_auto_promoting = False
        self.is_cleaning = False
        self.is_resuming_after_clean = False
        self.resume_info = None
        self.is_resuming_live = False
        self.silence_task = None 
        self.is_playing_silence = False
        self.is_resuming_after_silence = False
        self.volume = 1.0
        self.controller_message_id = None
        self.duration_hydration_lock = asyncio.Lock()
        self.queue_lock = asyncio.Lock()
        self.silence_management_lock = asyncio.Lock()
        self.is_paused_by_leave = False
        self.manual_stop = False