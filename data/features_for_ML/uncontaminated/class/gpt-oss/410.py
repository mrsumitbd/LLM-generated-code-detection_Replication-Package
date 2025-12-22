class MusicPlayer:
    def __init__(self):
        self.playlist = []          # list of track names
        self.current_index = -1     # index of the current track
        self.is_playing = False     # True when a track is playing
        self.is_paused = False      # True when playback is paused
        self.volume = 50            # volume level (0-100)

    # Playlist management
    def add_track(self, track):
        """Add a track to the end of the playlist."""
        self.playlist.append(track)

    def remove_track(self, track):
        """Remove the first occurrence of a track from the playlist."""
        if track in self.playlist:
            idx = self.playlist.index(track)
            self.playlist.pop(idx)
            if idx <= self.current_index:
                self.current_index -= 1
            if not self.playlist:
                self.current_index = -1
                self.is_playing = False
                self.is_paused = False

    def get_playlist(self):
        """Return a copy of the current playlist."""
        return list(self.playlist)

    # Playback controls
    def play(self):
        """Start or resume playback."""
        if not self.playlist:
            return
        if self.is_paused:
            self.is_paused = False
        elif not self.is_playing:
            if self.current_index == -1:
                self.current_index = 0
            self.is_playing = True

    def pause(self):
        """Pause playback."""
        if self.is_playing:
            self.is_paused = True

    def stop(self):
        """Stop playback and reset to the beginning."""
        self.is_playing = False
        self.is_paused = False
        self.current_index = -1

    def next_track(self):
        """Skip to the next track."""
        if not self.playlist:
            return
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.is_playing = True
        self.is_paused = False

    def prev_track(self):
        """Return to the previous track."""
        if not self.playlist:
            return
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.is_playing = True
        self.is_paused = False

    # Volume control
    def set_volume(self, level):
        """Set volume (clamped between 0 and 100)."""
        self.volume = max(0, min(100, level))

    def get_volume(self):
        """Return the current volume level."""
        return self.volume

    # Current track information
    def get_current_track(self):
        """Return the name of the current track, or None if stopped."""
        if self.current_index == -1:
            return None
        return self.playlist[self.current_index]

    # Representation
    def __repr__(self):
        status = "stopped"
        if self.is_playing:
            status = "paused" if self.is_paused else "playing"
        return (
            f"<MusicPlayer status={status} "
            f"track={self.get_current_track()} "
            f"volume={self.volume}>"
        )